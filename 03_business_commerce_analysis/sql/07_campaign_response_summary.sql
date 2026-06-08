-- Campaign response rate based on target household table and coupon redemption table.
-- This is observed redemption response, not causal promotion lift.
WITH target AS (
  SELECT CAMPAIGN, DESCRIPTION, COUNT(DISTINCT household_key) AS target_households
  FROM campaign_table
  GROUP BY CAMPAIGN, DESCRIPTION
), redemptions AS (
  SELECT CAMPAIGN, COUNT(DISTINCT household_key) AS redeemed_households, COUNT(*) AS redemptions
  FROM coupon_redempt
  GROUP BY CAMPAIGN
)
SELECT
  t.CAMPAIGN, t.DESCRIPTION, d.START_DAY, d.END_DAY,
  t.target_households, COALESCE(r.redeemed_households, 0) AS redeemed_households,
  COALESCE(r.redemptions, 0) AS redemptions,
  COALESCE(r.redeemed_households, 0) * 1.0 / NULLIF(t.target_households, 0) AS response_rate_observed
FROM target t
LEFT JOIN redemptions r ON t.CAMPAIGN = r.CAMPAIGN
LEFT JOIN campaign_desc d ON t.CAMPAIGN = d.CAMPAIGN AND t.DESCRIPTION = d.DESCRIPTION
ORDER BY response_rate_observed DESC;
