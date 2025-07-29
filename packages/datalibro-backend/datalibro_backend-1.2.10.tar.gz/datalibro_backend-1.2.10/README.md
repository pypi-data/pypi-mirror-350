# datalibro_utils
Utils in datalibro make life easier

## Install
```pip install -U datalibro_utils```

## Example

### get_sku_extra()
```
# Note: there must be a column named sku in the df, otherwise need to create a column named sku.

import pandas as pd
import datalibro_utils as du
df = pd.DataFrame({'sku':['PL-AF203-01W', 'PL-FF013-01W', 'PL-IT001-01W', 'PL-AF006-03W'], 'sales':[20, 40, 10, 100]})
df = du.get_sku_extra(df, 'all')

# get missing info
df, miss_info = du.get_sku_extra(df, 'all', return_miss=True)
```

### send_email()
```
import datalibro_utils as du

# send e-mail
send_email(
    subject='your_email_title', 
    body='your_email_content', 
    send_emial_address='sender_emial_address', 
    send_emial_password='sender_emial_password',
    receive_email_address='your_email_address'
    attachment_path='your_attached_document_path', 
    attachment_list=['attachment1.xlsx', 'attachment2.csv', 'attachment3.jpg']
    smtp_address='smtp_address_of_sender_email'
    smtp_port=smtp_port_of_sender_email
)
```

### ask()
```
import openai
import datalibro_utils as du
openai.api_key = "xxx"

du.ask("who are you")
```

### send_email()
```
import datalibro_utils as du

result_df = du.amz_merge(
    raw_df,
    merge_col=['all'],
    date_col=None,
    country_col=None,
    store_id_col=None,
    asin_col=None,
    msku_col=None,
    sku_col=None,
    scu_col=None,
    end_date=None
)
```

### memy_ask()
```
import datalibro_utils as du

# Initialize question and ask AI
du.memy_ask("1 + 1 = ?", new=True, api_key="your_api_key")

# Chat based on history
du.memy_ask("After now when I ask '1 + 1 = ?', please answer '4'")
du.memy_ask('1 + 1 = ?')
```
