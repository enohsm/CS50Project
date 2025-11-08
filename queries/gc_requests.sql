SELECT
    gc_requests.id AS id,
    vehicles.plate AS plate,
    gc_requests.start_date AS startdate,
    gc_requests.cov_period AS cov_period,
    gc_requests.request_date AS request_date,
    gc_requests.status AS stat
FROM vehicles
JOIN gc_requests
    ON vehicles.id = gc_requests.vehicle_id
WHERE vehicles.user_id = ?
ORDER BY request_date DESC