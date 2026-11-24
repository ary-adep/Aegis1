Apply database migrations before deploying workers. During a rollout,
previous worker and consumer versions remain active until the new workers
are ready. Deployment may roll back to the previous worker image.
