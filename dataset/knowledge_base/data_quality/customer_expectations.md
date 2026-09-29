# Customer Data Quality

customer_id must be non-null and unique. Email may be null. Country should match ISO-2 when present. Schema parser rejects malformed CSV rows into quarantine instead of shifting columns.
