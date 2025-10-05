Part 1: OCR reader for reading contact lense paramters and brands 
Features:
    - OCR parses title and parameter values from contact lens label
    - BC and DIAM retrieved from OD SPECS 
    - Error handling, if values/ info is missing
    - Create Camera Guide for snapshots for contact lens alignment


Part 2: Database for live stocking
Features:
    - Logs each contact lens that is scanned
        - removes from database if given to patient 
        - adds to database if stock arrived
    - Notifies if stock is running low
        - creates/suggests stock order sheet
    - If new duplicate stock is being ordered when it was ordered less than 2 weeks ago, 
    a warning is shown to prevent overstocking 



Part 3: Visual manual stocking
Features:
    - Create tap to order with visual layout for easy ordering
    - Will log orders onto database 
    - Can print out order sheet 
    - possible automation for ordering through corresponding brand website
