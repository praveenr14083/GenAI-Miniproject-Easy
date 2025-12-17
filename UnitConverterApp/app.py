import streamlit as st

st.set_page_config(page_title="Unit Converter", layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

st.title(" Unit Converter App")

unit_converter=st.selectbox("Select Conversion Type", ["Distance", "Temperature", "Weight", "Currency"])


if unit_converter=="Distance":

    st.subheader("Distance")
    km = st.number_input("Kilometers", value=0.0, key="km")
    if st.button("Convert KM → Miles"):
        miles = km * 0.621371
        result = f"{km} km = {miles:.2f} miles"
        st.success(result)
        st.session_state.history.append(result)

    miles_in = st.number_input("Miles", value=0.0, key="miles")
    if st.button("Convert Miles → KM"):
        km_out = miles_in / 0.621371
        result = f"{miles_in} miles = {km_out:.2f} km"
        st.success(result)
        st.session_state.history.append(result)

elif unit_converter=="Temperature":
    st.subheader("Temperature")
    c = st.number_input("Celsius", value=0.0, key="c")
    if st.button("Convert °C → °F"):
        f = (c * 9 / 5) + 32
        result = f"{c} °C = {f:.2f} °F"
        st.success(result)
        st.session_state.history.append(result)

    f_in = st.number_input("Fahrenheit", value=32.0, key="f")
    if st.button("Convert °F → °C"):
        c_out = (f_in - 32) * 5 / 9
        result = f"{f_in} °F = {c_out:.2f} °C"
        st.success(result)
        st.session_state.history.append(result)

elif unit_converter=="Weight":
    st.subheader("Weight")
    kg = st.number_input("Kilograms", value=0.0, key="kg")
    if st.button("Convert KG → Pounds"):
        pounds = kg * 2.20462
        result = f"{kg} kg = {pounds:.2f} lbs"
        st.success(result)
        st.session_state.history.append(result)

    lbs = st.number_input("Pounds", value=0.0, key="lbs")
    if st.button("Convert Pounds → KG"):
        kg_out = lbs / 2.20462
        result = f"{lbs} lbs = {kg_out:.2f} kg"
        st.success(result)
        st.session_state.history.append(result)


elif unit_converter=="Currency":
    st.subheader("Currency")
    st.caption("1 USD = ₹83")

    inr = st.number_input("Rupees (INR)", value=0.0, key="inr")
    if st.button("Convert INR → USD"):
        usd = inr / 83
        result = f"₹{inr} = ${usd:.2f}"
        st.success(result)
        st.session_state.history.append(result)

    usd_in = st.number_input("USD", value=0.0, key="usd")
    if st.button("Convert USD → INR"):
        inr_out = usd_in * 83
        result = f"${usd_in} = ₹{inr_out:.2f}"
        st.success(result)
        st.session_state.history.append(result)


st.subheader(" Conversion History")
with st.expander("History"):
    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history), start=1):
            st.write(f"{i}. {item}")
    else:
        st.info("No conversions yet")

if st.button("Clear History"):
    st.session_state.history.clear()
    st.success("History cleared")
