Part 1: OCR reader for reading contact lense paramters and brands 
Features:
    - OCR parses title and parameter values from contact lens label
    - BC and DIAM retrieved from OD SPECS 
    - Error handling, if values/ info is missing
    - Create Camera Guide for snapshots for contact lens alignment


Part 2: Database for live stocking
Features:
    - LOGGING:
        - Logs each contact lens that is scanned
        - Updates status of contact lens when patient picked up 
        - adds to database if stock arrived
    - Manual ordering sheet for pt
        - Add Autofill based on contact lens brand
        - Add Options for Drs and Brands
    - Notifies if stock is running low
        - creates/suggests stock order sheet
    - Sort all orders by:
        a. DEFAULT: DESC by date 
        b. ASC and DESC by date
        c. ASC and DESC arrival_date 
    - Filter orders by:
        a. Brand 
        b. Patient 
        c. Order Date
        d. arrival Date
        e. type 
        f. doctor
    - Search by:
        a. order id 
        b. patient name 
    - If new duplicate stock is being ordered when it was ordered less than 2 weeks ago, 
    a warning is shown to prevent overstocking 



Part 3: Visual manual stocking
Features:
    - Create tap to order with visual layout for easy ordering
    - Will log orders onto database 
    - Can print out order sheet 
    - possible automation for ordering through corresponding brand website


'''
data = {
    "Brand" : "Acuvue Oasys",
    "Sphere" : -2.25,
    "Cyl" : -0.75,
    "Axis" : 180,
    "Patient_Name" : "John Doe",
    "PID" : "12345"
    }
'''