from flask import Blueprint, jsonify, request
from utils.data_loader import get_frequencies_by_version, load_limits
from utils.data_loader import get_antenna_factor

emission_bp = Blueprint('emission', __name__)

@emission_bp.route('/api/re102/calibration', methods=['GET'])
def get_calibration_values():
    """API for calculating calibration field strength (limits - 6 dB) for all limit lines."""
    standard_version = request.args.get("version")
    category_name = request.args.get("category")

    if not standard_version or not category_name:
        return jsonify({"error": "Missing 'version' or 'category' parameter"}), 400

    # Get control frequencies
    frequencies = get_frequencies_by_version(standard_version)
    if not frequencies:
        return jsonify({"error": f"No frequencies found for version {standard_version}"}), 404

    # Get limits for the selected category
    all_limits = load_limits()
    category = next((c for c in all_limits["categories"] if category_name in c["name"]), None)
    if not category:
        return jsonify({"error": f"No limits found for category {category_name}"}), 404

    results = []
    for limit_group in category["limits"]:  # Each sub-category (limit line)
        limit_line_name = limit_group["sub_category"]
        calibration_data = []

        for freq in frequencies:
            closest_limit = min(limit_group["data"], key=lambda x: abs(x["frequency_mhz"] - freq))
            calibration_value = closest_limit["limit_dbuv_m"] - 6
            calibration_data.append({
                "frequency_mhz": freq,
                "original_limit_dbuv_m": closest_limit["limit_dbuv_m"],
                "calibration_dbuv_m": calibration_value
            })

        results.append({
            "limit_line": limit_line_name,
            "calibration_data": calibration_data
        })

    return jsonify(results)

@emission_bp.route('/api/re102/frequencies', methods=['GET'])
def get_frequencies():
    """API endpoint for getting RE102 control frequencies based on MIL-STD-461 version."""
    standard_version = request.args.get("version")

    if not standard_version:
        return jsonify({"error": "Missing 'version' parameter"}), 400

    frequencies = get_frequencies_by_version(standard_version)

    if not frequencies:
        return jsonify({"error": f"No frequencies found for version {standard_version}"}), 404

    return jsonify({"version": standard_version, "frequencies": frequencies})

@emission_bp.route('/api/re102/antenna-factor', methods=['GET'])
def get_antenna_factor_api():
    """API endpoint for getting antenna factor based on frequency."""
    antenna_type = request.args.get("antenna")
    frequency_mhz = request.args.get("frequency", type=float)

    if not antenna_type or frequency_mhz is None:
        return jsonify({"error": "Missing 'antenna' or 'frequency' parameter"}), 400

    factor = get_antenna_factor(antenna_type, frequency_mhz)
    if not factor:
        return jsonify({"error": f"Antenna '{antenna_type}' not found"}, 404)

    return jsonify(factor)

