from ldpc import bposd_decoder
import numpy as np
import src.helpers.linalg_helpers as linalg_help


def bposd_decode_distance_estimate(stabilizers, logicals, status_updates = False) -> int:
    best_distance = stabilizers.shape[1]

    for i, operator in enumerate(logicals):
        combined_matrix = np.vstack((stabilizers, operator))
        current_distance = stabilizers.shape[1]

        error_rates = [0.02, 0.03, 0.04]
        for error_rate in error_rates:
            bpd = bposd_decoder(
                parity_check_matrix=combined_matrix,
                error_rate=error_rate,
                channel_probs=[None],
                max_iter=combined_matrix.shape[1],  # The maximum number of iterations for BP
                bp_method="ms",
                ms_scaling_factor=0,  # Min sum scaling factor. If set to zero the variable scaling factor method is used
                osd_method="osd_cs",  # The OSD method. Choose from: 1) "osd_e", "osd_cs", "osd0"
                osd_order=10  # The osd search depth
            )

            syndrome = np.array([0] * stabilizers.shape[0] + [1])
            current_distance = min(current_distance, sum(bpd.decode(syndrome)))

            if status_updates:
                print(f"For logical of weight: {sum(operator)} and error_rate {error_rate}, distance: {current_distance}")

        best_distance = min(best_distance, current_distance)

    return best_distance



def calculate_distance(H_x, H_z, status_updates = False) -> int:
    stabilizers = linalg_help.standard_form(H_x, H_z)

    Lx, Lz = linalg_help.find_logical_generators(
        stabilizers,
        linalg_help.binary_rank(H_x)
    )
    logicals = np.vstack((Lx, Lz))

    return bposd_decode_distance_estimate(stabilizers, logicals, status_updates = status_updates)



