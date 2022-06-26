
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
        # Table Name (varchar)
        # Table ID (varchar)
        # List of Params List ID (varchar)
        # Created AT
        # Updated AT
    
    ## List (list_table) (DONE)
        # List ID ()
        # item_index
        # value
        # value_type
        ## List ID and Index are together primary key
    
    ## Inventory Table Structure (inventory_table)
        # Table ID
        # Param Values List ID
        # Created AT
        # Updated AT
        
# Table Create commands
## Database
```CREATE DB inventory_management```
## List of Tables
List Table
```CREATE TABLE list_table (list_id VARCHAR(255) NOT NULL, item_index INT NOT NULL, value VARCHAR(255), value_type VARCHAR(255), PRIMARY KEY(list_id, item_index));```

Inventory Table
```CREATE TABLE inventory_table (table_id VARCHAR(255) NOT NULL,list_id VARCHAR(255) NOT NULL,created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,updated_at TIMESTAMP NOT NULL DEFAULT now() ON UPDATE now(),PRIMARY KEY(table_id, list_id));```

Metadata Table
```CREATE TABLE metadata_table (table_id VARCHAR(255) NOT NULL,table_name VARCHAR(255) NOT NULL,list_id_params VARCHAR(255) NOT NULL,created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,updated_at TIMESTAMP NOT NULL DEFAULT now() ON UPDATE now(),PRIMARY KEY(table_id));```