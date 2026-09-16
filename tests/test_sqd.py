from quantum_workflows.sqd import is_valid_configuration


def test_sqd_configuration_symmetry_check() -> None:
    # Four orbitals per spin sector, two alpha and two beta electrons.
    assert is_valid_configuration("00110011", 4, (2, 2))
    assert not is_valid_configuration("00110001", 4, (2, 2))
    assert not is_valid_configuration("0011", 4, (2, 2))
