# Stage 3 — Data Extraction

## Purpose
Extract reusable analytical fields from validated source columns.

### Temporal fields
- Booking_DateTime
- Booking_Hour
- Booking_Day
- Booking_Month
- Booking_Weekday
- Is_Weekend
- Time_of_Day

### Business fields
- Is_Completed
- Is_Cancelled
- Is_Unfulfilled
- Is_Incomplete
- Cancellation_Type
- Revenue_per_km
- High_Value_Ride
- Wait_Time_Category
- Distance_Category
- Avg_Rating
- Rating_Category

Derived fields must be deterministic and must not invent observations for missing source values.
