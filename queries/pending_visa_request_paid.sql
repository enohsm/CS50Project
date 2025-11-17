SELECT 
    visa.id
FROM visa_requests AS visa
WHERE visa.status = 0
    AND visa.id = ?
    AND visa.payment_status = 1