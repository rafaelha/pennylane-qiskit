import numpy as np
import pytest

import pennylane as qml
from pennylane_qiskit import AerDevice


class TestProbabilities:
    """Tests for the probability function"""

    def test_probability_no_results(self):
        """Test that the probabilities function returns
        None if no job has yet been run."""
        dev = AerDevice(backend="statevector_simulator", wires=1, analytic=True)
        assert dev.probabilities() is None


class TestAnalyticWarningHWSimulator:
    """Tests the warnings for when the analytic attribute of a device is set to true"""

    def test_warning_raised_for_hardware_backend_analytic_expval(self, hardware_backend, recorder):
        """Tests that a warning is raised if the analytic attribute is true on
            hardware simulators when calculating the expectation"""

        dev = qml.device("qiskit.basicaer", backend=hardware_backend, wires=2, analytic=True)

        @qml.qnode(dev)
        def circuit():
            qml.Hadamard(wires=0)
            return qml.expval(qml.PauliZ(0))

        with pytest.warns(UserWarning) as record:
            circuit()

        # check that only one warning was raised
        assert len(record) == 1
        # check that the message matches
        assert record[0].message.args[0] == "The analytic calculation of expectations and variances "\
                                            "is only supported on statevector backends, not on the {}. "\
                                            "The obtained result is based on sampling.".format(dev.backend)

    def test_no_warning_raised_for_software_backend_analytic_expval(self, statevector_backend, recorder, recwarn):
        """Tests that no warning is raised if the analytic attribute is true on
            statevector simulators when calculating the expectation"""

        dev = qml.device("qiskit.basicaer", backend=statevector_backend, wires=2, analytic=True)

        @qml.qnode(dev)
        def circuit():
            qml.Hadamard(wires=0)
            return qml.expval(qml.PauliZ(0))

        circuit()

        # check that no warnings were raised
        assert len(recwarn) == 0

    def test_warning_raised_for_hardware_backend_analytic_var(self, hardware_backend, recorder):
        """Tests that a warning is raised if the analytic attribute is true on
            hardware simulators when calculating the variance"""

        dev = qml.device("qiskit.basicaer", backend=hardware_backend, wires=2, analytic=True)

        @qml.qnode(dev)
        def circuit():
            qml.Hadamard(wires=0)
            return qml.var(qml.PauliZ(0))

        with pytest.warns(UserWarning) as record:
            circuit()

        # check that only one warning was raised
        assert len(record) == 1
        # check that the message matches
        assert record[0].message.args[0] == "The analytic calculation of expectations and variances "\
                                            "is only supported on statevector backends, not on the {}. "\
                                            "The obtained result is based on sampling.".format(dev.backend)

    def test_no_warning_raised_for_software_backend_analytic_var(self, statevector_backend, recorder, recwarn):
        """Tests that no warning is raised if the analytic attribute is true on
            statevector simulators when calculating the variance"""

        dev = qml.device("qiskit.basicaer", backend=statevector_backend, wires=2, analytic=True)

        @qml.qnode(dev)
        def circuit():
            qml.Hadamard(wires=0)
            return qml.var(qml.PauliZ(0))

        circuit()

        # check that no warnings were raised
        assert len(recwarn) == 0
