import pandas as pd

# Sample data
data = {
    'Phone': ['1234567890', '9876543210', '1112223333', '4445556666'],
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Text': ['Hello Alice!', 'Hi Bob!', 'Hey Charlie!', 'Hi David!'],
    'Other Message': [
        'This is another message for Alice.',
        'Another message for Bob.',
        'Message for Charlie.',
        'Extra message for David.'
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save as CSV
df.to_csv('contacts_with_messages.csv', index=False)

# Save as XLSX
df.to_excel('contacts_with_messages.xlsx', index=False)
