-- API key management functions
CREATE OR REPLACE FUNCTION generate_api_key()
    RETURNS text
    LANGUAGE sql
AS $$
    SELECT encode(gen_random_bytes(32), 'hex');
$$;

CREATE OR REPLACE FUNCTION hash_api_key(api_key text)
    RETURNS text
    LANGUAGE sql
AS $$
    SELECT crypt(api_key, gen_salt('bf'));
$$;

CREATE OR REPLACE FUNCTION check_api_key(api_key text)
    RETURNS uuid
    LANGUAGE plpgsql
    SECURITY DEFINER
AS $$
DECLARE
    user_id uuid;
BEGIN
    SELECT ak.user_id INTO user_id
    FROM api_keys ak
    WHERE ak.key_hash = crypt(api_key, ak.key_hash)
    AND NOT ak.revoked
    LIMIT 1;
    
    IF user_id IS NULL THEN
        RETURN NULL;
    END IF;
    
    UPDATE api_keys
    SET last_used_at = NOW()
    WHERE key_hash = crypt(api_key, key_hash);
    
    RETURN user_id;
END;
$$;

-- Usage quota management functions
CREATE OR REPLACE FUNCTION check_usage_quota(user_id uuid)
    RETURNS boolean
    LANGUAGE plpgsql
    SECURITY DEFINER
AS $$
DECLARE
    quota_record usage_quotas%ROWTYPE;
BEGIN
    SELECT * INTO quota_record
    FROM usage_quotas
    WHERE usage_quotas.user_id = check_usage_quota.user_id
    FOR UPDATE;
    
    IF quota_record IS NULL THEN
        RETURN false;
    END IF;
    
    IF quota_record.current_usage >= quota_record.monthly_limit THEN
        RETURN false;
    END IF;
    
    UPDATE usage_quotas
    SET current_usage = current_usage + 1
    WHERE usage_quotas.user_id = check_usage_quota.user_id;
    
    RETURN true;
END;
$$;

CREATE OR REPLACE FUNCTION reset_monthly_quotas()
    RETURNS void
    LANGUAGE plpgsql
    SECURITY DEFINER
AS $$
BEGIN
    UPDATE usage_quotas
    SET current_usage = 0,
        reset_date = NOW()
    WHERE DATE_TRUNC('month', reset_date) < DATE_TRUNC('month', NOW());
END;
$$;