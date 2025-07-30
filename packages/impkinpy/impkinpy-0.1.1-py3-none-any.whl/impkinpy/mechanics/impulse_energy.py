import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.special import gamma

class Impulse_Energy():
    def impulse_k_energy(self, m: list[int | float], v0_vectors: list[list[int | float]]):
        impulse_list = []
        k_energy_list = []
        for i in range(len(m)):
            impulse = [v0_vectors[i][0] * m[i], v0_vectors[i][1] * m[i], v0_vectors[i][2] * m[i]]
            k_energy = m[i] * np.linalg.norm(v0_vectors[i]) ** 2 / 2

            impulse_list.append(impulse)
            k_energy_list.append(k_energy)

        return impulse_list, k_energy_list

    def all_impulse_k_energy(self, impulse_list: list[list[int | float]], k_energy_list: list[list[int | float]]):
        system_impulse = []
        for k in range(len(impulse_list) - 1):
            for l in range(len(impulse_list[k])):
                system_impulse.append(impulse_list[k][l] + impulse_list[k + 1][l])
        system_k_energy = np.sum(k_energy_list)

        return system_impulse, system_k_energy
    
    def impulse(self, m, v):
        return m * v
    
    def mass_center(self, mass_list: list[int | float], coords_list: list[list[int | float]], velocity_list: list[int | float]):
        coords = []
        velocity = []

        coords_dimension = len(coords_list[0])
        
        for i in range(len(coords_list)):
            for j in range(coords_dimension):
                coords.append(mass_list[i] * coords_list[i][j])
                velocity.append(mass_list[i] * velocity_list[i][j])

        x_list_c = []
        y_list_c = []
        x_list_v = []
        y_list_v = []

        for k in range(len(coords)):
            if k % 2 == 0:
                x_list_c.append(coords[k])
                x_list_v.append(velocity[k])
            else:
                y_list_c.append(coords[k])
                y_list_v.append(velocity[k])
        x_c = np.sum(x_list_c)
        y_c = np.sum(y_list_c)
        x_v = np.sum(x_list_v)
        y_v = np.sum(y_list_v)

        m_c_coords = [(1 / np.sum(mass_list)) * x_c, (1 / np.sum(mass_list)) * y_c]
        m_c_velocity = [(1 / np.sum(mass_list)) * x_v, (1 / np.sum(mass_list)) * y_v]
    
        return m_c_coords, m_c_velocity

    def rotate_coords_2D(self, coords_list: list[int | float], angle: int | float):
        if len(coords_list) == 2:
            x1 = coords_list[0] * np.cos(angle) - coords_list[1] * np.sin(angle)
            y1 = coords_list[0] * np.sin(angle) + coords_list[1] * np.cos(angle)
            
            return [x1, y1]
        
    def rotate_coords_3D(self, coords_list: list[int | float], angle: int | float, rotate_axes: list[str]):
        if len(coords_list) == 3:
            axes_dict = {"YZ": np.array([[1, 0, 0], 
                                        [0, np.cos(angle), -np.sin(angle)],
                                        [0, np.sin(angle), np.cos(angle)]]),
                        "XZ": np.array([[np.cos(angle), 0, np.sin(angle)], 
                                    [0, 1, 0],
                                    [-np.sin(angle), 0, np.cos(angle)]]),
                        "XY": np.array([[np.cos(angle), -np.sin(angle), 0],  
                                    [np.sin(angle), np.cos(angle), 0],
                                    [0, 0, 1]]),
                        "yz": np.array([[1, 0, 0], 
                                    [0, np.cos(angle), -np.sin(angle)],
                                    [0, np.sin(angle), np.cos(angle)]]),
                        "xz": np.array([[np.cos(angle), 0, np.sin(angle)],
                                    [0, 1, 0],
                                    [-np.sin(angle), 0, np.cos(angle)]]),
                        "xy": np.array([[np.cos(angle), -np.sin(angle), 0], 
                                    [np.sin(angle), np.cos(angle), 0],
                                    [0, 0, 1]])}
            
            rotate_axes = rotate_axes.split()
            rotate_axes = np.array(rotate_axes)

            coords = np.array(coords_list).reshape(3, 1)

            if len(rotate_axes) == 1:
                xyz = axes_dict[rotate_axes[0]] @ coords
            if len(rotate_axes) == 2:
                xyz = axes_dict[rotate_axes[0]] @ axes_dict[rotate_axes[1]] @ coords
            if len(rotate_axes) == 3:
                xyz = axes_dict[rotate_axes[0]] @ axes_dict[rotate_axes[1]] @ axes_dict[rotate_axes[2]] @ coords

            return [xyz[0][0], xyz[1][0], xyz[2][0]]

    def rotate_coords_nD(self, coords_list: list[int | float], angle: int | float, rotate_axes: list[str]):
        coords_dict = {}
        ij_list = []
        rotate_matrix = np.zeros((len(coords_list), len(coords_list)))
        for i in range(len(coords_list)):
            coords_dict[f"x{i + 1}"] = coords_list[i]
            coords_dict[f"X{i + 1}"] = coords_list[i]
            if f"x{i + 1}" == rotate_axes[0] or f"x{i + 1}"  == rotate_axes[1] or f"X{i + 1}" == rotate_axes[0] or f"X{i + 1}"  == rotate_axes[1]:
                ij_list.append(i + 1)
        for a in range(np.shape(rotate_matrix)[0]):
            for b in range(np.shape(rotate_matrix)[1]):
                if a == ij_list[0] and b == ij_list[1]:
                    rotate_matrix[a - 1][b - 1] = -np.sin(angle)
                if a == ij_list[1] and b == ij_list[0]:
                    rotate_matrix[a - 1][b - 1] = np.sin(angle)
                if a == ij_list[0] and b == ij_list[0]:
                    rotate_matrix[a - 1][b - 1] = np.cos(angle)
                if a == ij_list[1] and b == ij_list[1]:
                    rotate_matrix[a - 1][b - 1] = np.cos(angle)
                else:
                    for k in range(a):
                        rotate_matrix[a][a] = 1

        rotate_matrix = np.array(rotate_matrix)
        coords_list = np.array(coords_list)

        xyz = rotate_matrix @ coords_list

        return xyz
