import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import numba

@numba.njit
def es_calc_bolton(temp):
    # in hPa
    tmelt  = 273.15
    tempc = temp - tmelt
    es = 6.112 * np.exp( 17.67 * tempc / (243.5+tempc) )
    return es

@numba.njit
def es_calc(temp):
    tmelt  = 273.15
    c0=0.6105851e+03
    c1=0.4440316e+02
    c2=0.1430341e+01
    c3=0.2641412e-01
    c4=0.2995057e-03
    c5=0.2031998e-05
    c6=0.6936113e-08
    c7=0.2564861e-11
    c8=-.3704404e-13
    tempc = temp - tmelt
    if tempc < -80:
        # in Pa
        es=es_calc_bolton(temp)*100.
    else:
        # in Pa
        es=c0+tempc*(c1+tempc*(c2+tempc*(c3+tempc*(c4+tempc*(c5+tempc*(c6+tempc*(c7+tempc*c8)))))))
    return es

def calculate_theta_e(T, p, p0, q_v, q_l=0, q_i=0):
    """
    Calculate equivalent potential temperature (theta_e) based on the provided equations
    and using the exact constants from the reference table.

    Parameters:
    -----------
    T : float
        Temperature in Kelvin
    p : float
        Pressure in Pa
    p0 : float
        Reference pressure (typically 100,000 Pa)
    q_v : float
        Specific humidity of water vapor (kg/kg)
    q_l : float, optional
        Specific humidity of liquid water (kg/kg), default is 0
    q_i : float, optional
        Specific humidity of ice (kg/kg), default is 0

    Returns:
    --------
    float
        Equivalent potential temperature (theta_e) in Kelvin
    """
    # Physical constants (values from the provided table)
    R_d = 0.2870 * 1000    # Gas constant for dry air (J/kg/K)
    R_v = 0.4615 * 1000    # Gas constant for water vapor (J/kg/K)
    c_pd = 1.005 * 1000    # Specific heat of dry air at constant pressure (J/kg/K)
    c_pv = 1.865 * 1000    # Specific heat of water vapor at constant pressure (J/kg/K)
    c_pl = 4.219 * 1000    # Specific heat of liquid water (J/kg/K)
    c_pi = 2.097 * 1000    # Specific heat of ice (J/kg/K)
    L_v = 2500.9 * 1000    # Latent heat of vaporization (J/kg)
    L_i = 333.4 * 1000     # Latent heat of fusion (J/kg)
    T_t = 273.16           # Triple point temperature (K)

    q_t = q_v + q_l + q_i
    R = R_d + q_v * R_v - q_t * R_d # 2.5
    # Calculate the specific heat of the system
#    c_p = c_pd + q_v * (c_pv - c_pd) + q_l * (c_pl - c_pd) + q_i * (c_pi - c_pd)
    c_p = c_pd + q_v * (c_pl - c_pd) # 2.23

    R_e = (1 - q_t) * R_d # 2.30 lines
    epsilon = R_d / R_v
    p_v = p * q_v / (epsilon + (1. - epsilon) * q_v)
    p_s = es_calc(T)
    omega_e = np.power(R / R_e, R_e / c_p) * np.power(p_v / p_s, -q_v * R_v / c_p) # 2.43

    # Calculate estimated vapor pressure

    # Calculate the equivalent potential temperature # 2.67
    ice_factor = np.power(T / T_t, -q_i * (c_pl - c_pi) / c_p)
    theta_e = T * np.power(p0 / p, R_e / c_p) * ice_factor * omega_e * \
                np.exp((q_v * L_v) / (c_p * T) - (q_i * L_i) / (c_p * T_t))

    return theta_e

def main(file_path):
    """Main function to process the data file and calculate theta_e."""
    try:
        # Load the data from the text file, skipping the first line
        data = pd.read_csv(file_path, sep='\s+', skiprows=1, header=None)

        # Manually assign column names
        column_names = [
            'Height', 'Pressure', 'Temperature', 'Specific_Humidity',
            'Heating_Forcing', 'Moistening_Forcing', 'Longwave_Forcing',
            'Shortwave_Forcing', 'U', 'V'
        ]
        data.columns = column_names

        # Extract the relevant columns
        height = data['Height']
        pressure = data['Pressure']
        temperature = data['Temperature']
        specific_humidity = data['Specific_Humidity']

        # Reference pressure (standard sea level pressure in Pa)
        p0 = 100000.0

        # Calculate theta_e and theta_es for each level
        theta_e_values = []
        theta_es_values = []

        for i in range(len(height)):
            T = temperature[i]
            p = pressure[i]
            q_v = specific_humidity[i]

            # Determine q_i based on temperature (simplified approach)
            q_i = 0  # Assume no ice for this example
            q_l = 0  # Assume no liquid water for this example

            # Calculate theta_e
            theta_e = calculate_theta_e(T, p, p0, q_v, q_l, q_i)
            theta_e_values.append(theta_e)

            # Calculate es and qs
            es = es_calc(T)
            qs = 0.622 * es / (p - (1 - 0.622) * es)

            # Calculate theta_es
            theta_es = calculate_theta_e(T, p, p0, qs, q_l, q_i)
            theta_es_values.append(theta_es)

        # Create a DataFrame with results
        results = pd.DataFrame({
            'Height (m)': height,
            'Pressure (Pa)': pressure,
            'Temperature (K)': temperature,
            'Specific Humidity (kg/kg)': specific_humidity,
            'Theta_e (K)': theta_e_values,
            'Theta_es (K)': theta_es_values
        })

        # Print the results
        print("\nResults (first few rows):")
        print(results.head())

        # Plot the vertical profile of theta_e and theta_es
        plt.figure(figsize=(10, 8))
        plt.plot(theta_e_values, height, 'b-', linewidth=2, label='Theta_e')
        plt.plot(theta_es_values, height, 'r--', linewidth=2, label='Theta_es')
        plt.xlabel('Equivalent Potential Temperature [K]')
        plt.ylabel('Height [km]')
        plt.title('Vertical Profile of Equivalent Potential Temperature')
        plt.grid(True)
        plt.xlim(330, 355)
        plt.ylim(0, 15000)  # Limit y-axis to 15 km
        plt.gca().set_yticks(np.arange(0, 16000, 1000))
        plt.gca().set_yticklabels(np.arange(0, 16, 1))
        plt.legend()
        plt.tight_layout()

        # Save the plot
        plt.savefig('theta_e_profile.png')
        print("Plot saved as 'theta_e_profile.png'")

        # Print statistical summary
        print("\nStatistical Summary of Theta_e:")
        print(f"Min: {min(theta_e_values):.2f} K")
        print(f"Max: {max(theta_e_values):.2f} K")
        print(f"Mean: {np.mean(theta_e_values):.2f} K")
        print(f"Standard Deviation: {np.std(theta_e_values):.2f} K")

        # Identify levels with maximum and minimum theta_e
        max_idx = theta_e_values.index(max(theta_e_values))
        min_idx = theta_e_values.index(min(theta_e_values))

        print(f"\nMaximum Theta_e: {max(theta_e_values):.2f} K at height {height[max_idx]:.2f} m (Level {max_idx+1})")
        print(f"Minimum Theta_e: {min(theta_e_values):.2f} K at height {height[min_idx]:.2f} m (Level {min_idx+1})")

        # Save results to CSV
        output_file = 'theta_e_results.csv'
        results.to_csv(output_file, index=False)
        print(f"\nResults saved to '{output_file}'")

        return results

    except Exception as e:
        print(f"An error occurred: {str(e)}")

        # Alternative approach if column names are causing issues
        print("\nTrying alternative approach with fixed column assignments...")
        try:
            # Try to read without headers and assign our own column names
            data = pd.read_csv(file_path, sep='\s+', header=None)

            # Assuming column order from the error message:
            # Height, Pressure, Temperature, Specific Humidity, ... (other columns)
            column_names = ['Height', 'Pressure', 'Temperature', 'Specific_Humidity']
            column_names += [f'Column_{i+5}' for i in range(len(data.columns)-4)]

            data.columns = column_names

            # Continue with calculations
            height = data['Height']
            pressure = data['Pressure']
            temperature = data['Temperature']
            specific_humidity = data['Specific_Humidity']

            # Reference pressure (standard sea level pressure in Pa)
            p0 = 100000.0

            # Calculate theta_e for each level
            theta_e_values = []

            for i in range(len(height)):
                T = temperature[i]
                p = pressure[i]
                q_v = specific_humidity[i]

                q_i = 0  # Assume no ice for this example
                q_l = 0  # Assume no liquid water for this example

                # Calculate theta_e
                theta_e = calculate_theta_e(T, p, p0, q_v, q_l, q_i)
                theta_e_values.append(theta_e)

            # Create a DataFrame with results
            results = pd.DataFrame({
                'Height (m)': height,
                'Pressure (Pa)': pressure,
                'Temperature (K)': temperature,
                'Specific Humidity (kg/kg)': specific_humidity,
                'Theta_e (K)': theta_e_values
            })

            # Print the results
            print("\nResults (first few rows):")
            print(results.head())

            # Save results to CSV
            output_file = 'theta_e_results.csv'
            results.to_csv(output_file, index=False)
            print(f"\nResults saved to '{output_file}'")

            return results

        except Exception as nested_e:
            print(f"Alternative approach also failed: {str(nested_e)}")
            print("\nPlease check the format of your input file and try again.")
            return None

if __name__ == "__main__":
    path = '/data/W.eddie/GoAmazon_VVM/'
    file_path = f'{path}inic_lin58.txt'

    print(f"Processing file: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")

    if os.path.exists(file_path):
        main(file_path)
    else:
        print(f"Error: File '{file_path}' not found.")
        print("Please make sure the file exists in the current directory.")
