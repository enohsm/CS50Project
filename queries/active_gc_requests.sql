SELECT 
    gc_requests.id AS id,
    gc_requests.start_date AS startdate,
    gc_requests.cov_period AS cov_period,
    vehicles.plate AS plate,
    vehicles.brand AS brand,
    vehicles.color AS color
FROM gc_requests
JOIN vehicles
    ON gc_requests.vehicle_id = vehicles.id
WHERE gc_requests.id = ?
    AND gc_requests.user_id = ?
    AND gc_requests.status = 0