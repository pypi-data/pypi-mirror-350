#include "../include/thread_pool.h"
#include "../include/json_utils.h"
#include <stdlib.h>
#include <stdio.h>

// Worker thread function
static void* worker_thread(void* arg) {
    ThreadPool* pool = (ThreadPool*)arg;
    Task* task;
    
    while (1) {
        // Lock the queue mutex
        pthread_mutex_lock(&pool->queue_mutex);
        
        // Wait for a task or shutdown signal
        while (pool->task_queue == NULL && !pool->shutdown) {
            pthread_cond_wait(&pool->queue_cond, &pool->queue_mutex);
        }
        
        // Check for shutdown
        if (pool->shutdown && pool->task_queue == NULL) {
            pthread_mutex_unlock(&pool->queue_mutex);
            pthread_exit(NULL);
        }
        
        // Get a task from the queue
        task = pool->task_queue;
        if (task != NULL) {
            pool->task_queue = task->next;
            if (pool->task_queue == NULL) {
                pool->task_queue_tail = NULL;
            }
            pool->active_threads++;
        }
        
        pthread_mutex_unlock(&pool->queue_mutex);
        
        // Execute the task
        if (task != NULL) {
            task->function(task->argument);
            free(task);
            
            // Mark thread as idle
            pthread_mutex_lock(&pool->queue_mutex);
            pool->active_threads--;
            if (pool->active_threads == 0) {
                pthread_cond_signal(&pool->idle_cond);
            }
            pthread_mutex_unlock(&pool->queue_mutex);
        }
    }
    
    return NULL;
}

// Create a thread pool
ThreadPool* thread_pool_create(int num_threads) {
    ThreadPool* pool = (ThreadPool*)malloc(sizeof(ThreadPool));
    if (pool == NULL) {
        return NULL;
    }
    
    // Initialize pool properties
    pool->task_queue = NULL;
    pool->task_queue_tail = NULL;
    pool->shutdown = false;
    pool->active_threads = 0;
    
    // Determine number of threads
    pool->num_threads = get_optimal_threads(num_threads);
    
    // Initialize mutex and condition variables
    pthread_mutex_init(&pool->queue_mutex, NULL);
    pthread_cond_init(&pool->queue_cond, NULL);
    pthread_cond_init(&pool->idle_cond, NULL);
    
    // Allocate and create threads
    pool->threads = (pthread_t*)malloc(pool->num_threads * sizeof(pthread_t));
    if (pool->threads == NULL) {
        free(pool);
        return NULL;
    }
    
    for (int i = 0; i < pool->num_threads; i++) {
        if (pthread_create(&pool->threads[i], NULL, worker_thread, pool) != 0) {
            // Failed to create thread, clean up and return NULL
            thread_pool_destroy(pool);
            return NULL;
        }
    }
    
    return pool;
}

// Add a task to the thread pool
int thread_pool_add_task(ThreadPool* pool, void (*function)(void*), void* argument) {
    if (pool == NULL || function == NULL) {
        return -1;
    }
    
    // Create a new task
    Task* task = (Task*)malloc(sizeof(Task));
    if (task == NULL) {
        return -1;
    }
    
    task->function = function;
    task->argument = argument;
    task->next = NULL;
    
    // Add the task to the queue
    pthread_mutex_lock(&pool->queue_mutex);
    
    if (pool->task_queue == NULL) {
        pool->task_queue = task;
        pool->task_queue_tail = task;
    } else {
        pool->task_queue_tail->next = task;
        pool->task_queue_tail = task;
    }
    
    // Signal a waiting thread
    pthread_cond_signal(&pool->queue_cond);
    
    pthread_mutex_unlock(&pool->queue_mutex);
    
    return 0;
}

// Wait for all tasks to complete
void thread_pool_wait(ThreadPool* pool) {
    if (pool == NULL) {
        return;
    }
    
    pthread_mutex_lock(&pool->queue_mutex);
    
    // Wait until all tasks are completed
    while (pool->task_queue != NULL || pool->active_threads > 0) {
        pthread_cond_wait(&pool->idle_cond, &pool->queue_mutex);
    }
    
    pthread_mutex_unlock(&pool->queue_mutex);
}

// Destroy the thread pool
void thread_pool_destroy(ThreadPool* pool) {
    if (pool == NULL) {
        return;
    }
    
    // Set shutdown flag
    pthread_mutex_lock(&pool->queue_mutex);
    pool->shutdown = true;
    pthread_cond_broadcast(&pool->queue_cond);
    pthread_mutex_unlock(&pool->queue_mutex);
    
    // Wait for threads to exit
    for (int i = 0; i < pool->num_threads; i++) {
        pthread_join(pool->threads[i], NULL);
    }
    
    // Free memory
    free(pool->threads);
    
    // Clean up tasks
    Task* task = pool->task_queue;
    while (task != NULL) {
        Task* next = task->next;
        free(task);
        task = next;
    }
    
    // Destroy mutex and condition variables
    pthread_mutex_destroy(&pool->queue_mutex);
    pthread_cond_destroy(&pool->queue_cond);
    pthread_cond_destroy(&pool->idle_cond);
    
    free(pool);
}

// Get the number of threads in the pool
int thread_pool_get_thread_count(ThreadPool* pool) {
    if (pool == NULL) {
        return 0;
    }
    return pool->num_threads;
}