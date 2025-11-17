SELECT
    visa.id,
    visa.country,
    pass.name,
    pass.surname,
    pass.pass_no,
    visa.status AS stat,
    visa.request_date,
    visa.appointment_date AS app_date,
    ref.reference_no AS ref_no
FROM visa_requests AS visa
JOIN passports AS pass
    ON visa.pass_id = pass.id
LEFT JOIN app_references AS ref
    ON visa.id = ref.request_id
WHERE visa.status = 2
ORDER BY visa.request_date