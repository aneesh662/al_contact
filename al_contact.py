import streamlit as st
import os
import pandas as pd  # Import pandas for table formatting

# File to store contacts
CONTACTS_FILE = "contacts.txt"

# Helper functions
def add_contact(reg_no, name, initial, place, contact1, contact2):
    with open(CONTACTS_FILE, "a") as file:
        file.write(f"{reg_no},{name},{initial},{place},{contact1},{contact2}\n")
    st.success(f"Contact {name} added successfully!")

def get_contacts():
    if not os.path.exists(CONTACTS_FILE):
        return []
    with open(CONTACTS_FILE, "r") as file:
        contacts = [line.strip().split(",") for line in file.readlines()]
    return contacts

def clean_contact_entry(contact):
    """Ensure each contact has exactly 6 fields, filling missing fields with 'N/A'."""
    while len(contact) < 6:
        contact.append("N/A")
    return contact

def search_contact(name):
    contacts = get_contacts()
    result = []
    for contact in contacts:
        contact = clean_contact_entry(contact)
        if contact[1].lower() == name.lower():  # Compare the Name field
            result.append(contact)
    return result

def delete_contact(name):
    contacts = get_contacts()
    updated_contacts = [clean_contact_entry(contact) for contact in contacts if contact[1].lower() != name.lower()]
    
    with open(CONTACTS_FILE, "w") as file:
        for contact in updated_contacts:
            file.write(f"{contact[0]},{contact[1]},{contact[2]},{contact[3]},{contact[4]},{contact[5]}\n")
    
    if len(contacts) != len(updated_contacts):
        st.success(f"Contact {name} deleted successfully!")
    else:
        st.error(f"Contact {name} not found.")

# Streamlit app starts here
st.title("📒 Contact Book")

menu = ["Add Contact", "View All Contacts", "Search Contact", "Delete Contact", "Exit"]
choice = st.sidebar.selectbox("Select an option", menu)

if choice == "Add Contact":
    st.subheader("Add a New Contact")
    reg_no = st.text_input("Enter Registration Number:")
    name = st.text_input("Enter Name:")
    initial = st.text_input("Enter Initial:")
    place = st.text_input("Enter Place:")
    contact1 = st.text_input("Enter Contact Number 1:")
    contact2 = st.text_input("Enter Contact Number 2:")
    
    if st.button("Add Contact"):
        if reg_no and name and initial and place and contact1 and contact2:
            add_contact(reg_no, name, initial, place, contact1, contact2)
        else:
            st.error("Please provide all the required information.")

elif choice == "View All Contacts":
    st.subheader("View All Contacts")
    contacts = get_contacts()
    
    if contacts:
        # Ensure all entries are cleaned (i.e., have exactly 6 fields)
        contacts = [clean_contact_entry(contact) for contact in contacts]
        
        # Convert the contacts list to a DataFrame for better table display
        df = pd.DataFrame(contacts, columns=["Reg.No", "Name", "Initial", "Place", "Contact1", "Contact2"])
        
        # Display the DataFrame as a table
        st.table(df)
    else:
        st.info("No contacts available.")

elif choice == "Search Contact":
    st.subheader("Search for a Contact")
    search_name = st.text_input("Enter the name to search:")
    
    if st.button("Search"):
        results = search_contact(search_name)
        if results:
            # Convert the search results to a DataFrame
            df = pd.DataFrame(results, columns=["Reg.No", "Name", "Initial", "Place", "Contact1", "Contact2"])
            st.table(df)
        else:
            st.error(f"Contact {search_name} not found.")

elif choice == "Delete Contact":
    st.subheader("Delete a Contact")
    delete_name = st.text_input("Enter the name to delete:")
    
    if st.button("Delete"):
        if delete_name:
            delete_contact(delete_name)
        else:
            st.error("Please provide a contact name to delete.")

elif choice == "Exit":
    st.write("Thank you for using the Contact Book app!")
    st.stop()
