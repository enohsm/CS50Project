SELECT
    gc_requests.id,
    gc_requests.vehicle_id,
    vehicles.plate,
    vehicles.namesurname,
    vehicles.address,
    vehicles.vin,
    vehicles.brand,
    vehicles.model,
    vehicles.color,
    gc_requests.start_date AS startdate,
    gc_requests.cov_period,
    gc_requests.status AS stat,
    gc_requests.request_date,
    vehicles.img
FROM gc_requests
JOIN vehicles
    ON gc_requests.vehicle_id = vehicles.id
WHERE gc_requests.status = 0
    AND gc_requests.id = ?