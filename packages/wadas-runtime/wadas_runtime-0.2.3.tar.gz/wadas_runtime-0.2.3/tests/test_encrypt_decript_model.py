import wadas_runtime as wadas
import openvino as ov
import numpy as np
from wadas_encrypt import encrypt_model
import pytest
import os


@pytest.fixture(scope="module")
@pytest.mark.parametrize("device", ["CPU", "AUTO"])
def ov_model(device="CPU") -> tuple:
    """
    Creates an OpenVINO model, compiles it for the specified device, and serializes it to an XML file.
    Returns:
        tuple: A tuple containing:
            - example_input (numpy.ndarray): A randomly generated input tensor for the model.
            - reference_output (numpy.ndarray): The output tensor produced by the compiled model for the example input.
            - device (str): The name of the device used for compilation.
    """
    parm = ov.op.Parameter(ov.Type.f32, ov.Shape([64, 256]))

    data_bin = np.random.rand(256, 128).astype(np.float32)
    data = ov.op.Constant(ov.Type.f32, ov.Shape(data_bin.shape), data_bin.flatten())

    matmul = ov.opset1.matmul(parm, data, False, False)

    model = ov.Model(matmul, [parm])

    compiled_model = ov.compile_model(model, device)

    example_input = np.random.rand(64, 256).astype(np.float32)
    reference_output = compiled_model(example_input)[0]

    ov.serialize(model, "test_model.xml")

    return example_input, reference_output, device


def test_encryption_decription(ov_model):

    # Create and serialize the model
    example_input, reference_output, device = ov_model

    # Encrypt the model (this is done on the server side)
    encrypt_model("test_model.bin", "test_model_encrypted.bin")

    compiled_model_wadas = wadas.load_and_compile_model(
        "test_model.xml", "test_model_encrypted.bin", device
    )

    output = compiled_model_wadas(example_input)[0]

    assert np.allclose(
        output, reference_output
    ), "Decrypted model output does not match the original model output."


def test_no_encryption(ov_model):
    # Generate RSA keys
    example_input, reference_output, device = ov_model

    compiled_model_wadas = wadas.load_and_compile_model(
        "test_model.xml", device_name=device
    )

    output = compiled_model_wadas(example_input)[0]

    assert np.allclose(
        output, reference_output
    ), "Decrypted model output does not match the original model output."


def teardown_module(module):
    # Remove files created by tests
    for fname in ["test_model.xml", "test_model.bin", "test_model_encrypted.bin"]:
        try:
            os.remove(fname)
        except FileNotFoundError:
            pass
