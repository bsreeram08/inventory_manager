
# Inventory management Initiation

## Create an inventory
    # Defaults
        # SNO
        # Created AT
        # Updated AT
    # Custom Parameters
        # parameter name
        # parameter type
        
## Use existing inventory
    # Create/Write
    # Read
    # Update
    # Delete

# TABLE STRUCTURE TO ACHIEVE THIS
    ## Metadata Table (metadata_table)
        # SNO (int)
        # Table Name (varchar)
        # List of Params List ID (varchar)
    
    ## List (list_table)
        # List ID ()
        # item_index
        # value
        # value_type
        ## List ID and Index are together primary key
    
    ## Inventory Table Structure
        # SNO
        # Param Values List ID
        # Created AT
        # Updated AT
        
# Table Create commands
## Database
```CREATE DB inventory_management```
## List Table
```CREATE TABLE list_table (list_id VARCHAR(255) NOT NULL, item_index INT NOT NULL, value VARCHAR(255), value_type VARCHAR(255), PRIMARY KEY(list_id, item_index));```