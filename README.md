# Hospital Information API

##
This API connects to an Amazon RDS MySQL database that has been populated with data from the CMS API.
Submit GET requests for the requests fields in JSON format and a JSON object will be returned, reference 
below request.

When run locally navigate to http://localhost:5000/apidocs/ to access SWAGGER-UI API docs.

This API is also set up on an AWS EC2 instance using docker for containerization.

### Valid URLs:
```
/hospitals/{states}
/hospitals/{cities}
/hospitals/{zipcodes}
/hospitals/{facility_name}
/hospitals/{facility_ids}
```
#### Example Input:
```
{
    "facility_ids": ["100023"]
}
```
#### Example Output:

```
{"Status Code": 200,
    "myCollection": [
        {
            "Address": "502 W HIGHLAND BLVD",
            "City": "INVERNESS",
            "County_Name": "CITRUS",
            "Effectiveness_of_Care_National_Comparison": "Above the national average",
            "Efficient_Use_of_Medical_Imaging_National_Comparison": "Same as the national average",
            "Emergency_Services": "Yes",
            "Facility_ID": "100023",
            "Facility_Name": "CITRUS MEMORIAL HOSPITAL",
            "Hospital_Overall_Rating": "2",
            "Hospital_Ownership": "Government - Hospital District or Authority",
            "Hospital_Type": "Acute Care Hospitals",
            "Meets_criteria_for_promoting_interoperability_of_EHRs": "Y",
            "Mortality_National_Comparison": "Below the national average",
            "Patient_Experience_National_Comparison": "Below the national average",
            "Phone_Number": "(352) 726-1551",
            "Readmission_National_Comparison": "Below the national average",
            "Safety_of_Care_National_Comparison": "Above the national average",
            "State": "FL",
            "Timeliness_of_Care_National_Comparison": "Below the national average",
            "ZIP_Code": 34452,
            "index": 3640
        }
    ]
}
```