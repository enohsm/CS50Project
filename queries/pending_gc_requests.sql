SELECT
    gc_requests.id,
    users.username,
    vehicles.plate,
    gc_requests.start_date AS startdate,
    gc_requests.cov_period,
    gc_requests.status AS stat,
    gc_requests.request_date
FROM gc_requests
JOIN users
    ON gc_requests.user_id = users.id
JOIN vehicles
    ON gc_requests.vehicle_id = vehicles.id
WHERE gc_requests.status != 2