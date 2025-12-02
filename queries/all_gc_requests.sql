SELECT
    vehicles.namesurname,
    vehicles.address,
    vehicles.plate,
    vehicles.vin,
    vehicles.brand,
    vehicles.model,
    vehicles.color,
    gc_requests.start_date AS startdate,
    gc_requests.cov_period,
    gc_requests.status AS stat,
    gc_requests.request_date
FROM gc_requests
JOIN vehicles
    ON gc_requests.vehicle_id = vehicles.id