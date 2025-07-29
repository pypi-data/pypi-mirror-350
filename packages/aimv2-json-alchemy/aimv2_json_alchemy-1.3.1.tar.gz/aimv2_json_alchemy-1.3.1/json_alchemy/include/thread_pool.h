#ifndef THREAD_POOL_H
#define THREAD_POOL_H

#include <pthread.h>
#include <stdbool.h>

/**
 * Task structure for thread pool
 */
typedef struct Task {
    void (*function)(void*);  // Function to execute
    void* argument;           // Argument to pass to the function
    struct Task* next;        // Next task in the queue
} Task;

/**
 * Thread pool structure
 */
typedef struct {
    pthread_t* threads;           // Array of worker threads
    Task* task_queue;             // Queue of tasks to be executed
    Task* task_queue_tail;        // Tail of the task queue for faster enqueuing
    int num_threads;              // Number of threads in the pool
    int active_threads;           // Number of currently active threads
    bool shutdown;                // Flag to indicate shutdown
    pthread_mutex_t queue_mutex;  // Mutex to protect the task queue
    pthread_cond_t queue_cond;    // Condition variable for task queue
    pthread_cond_t idle_cond;     // Condition variable for idle threads
} ThreadPool;

/**
 * Creates a new thread pool
 * 
 * @param num_threads Number of threads in the pool (0 for auto)
 * @return A new thread pool, or NULL on failure
 */
ThreadPool* thread_pool_create(int num_threads);

/**
 * Adds a task to the thread pool
 * 
 * @param pool The thread pool
 * @param function The function to execute
 * @param argument The argument to pass to the function
 * @return 0 on success, -1 on failure
 */
int thread_pool_add_task(ThreadPool* pool, void (*function)(void*), void* argument);

/**
 * Waits for all tasks to complete and destroys the thread pool
 * 
 * @param pool The thread pool
 */
void thread_pool_destroy(ThreadPool* pool);

/**
 * Waits for all tasks to complete
 * 
 * @param pool The thread pool
 */
void thread_pool_wait(ThreadPool* pool);

/**
 * Gets the number of threads in the pool
 * 
 * @param pool The thread pool
 * @return The number of threads
 */
int thread_pool_get_thread_count(ThreadPool* pool);

#endif /* THREAD_POOL_H */