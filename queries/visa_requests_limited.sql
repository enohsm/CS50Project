SELECT
    passports.pass_no AS pass_no,
    visa_requests.country AS country,
    visa_requests.visa_type AS app_type,
    visa_requests.prefferred_appointment_date AS pref_app_date,
    visa_requests.status AS stat
FROM visa_requests
JOIN passports
    ON visa_requests.pass_id = passports.id
WHERE visa_requests.user_id = ?
ORDER BY visa_requests.request_date DESC
LIMIT 5