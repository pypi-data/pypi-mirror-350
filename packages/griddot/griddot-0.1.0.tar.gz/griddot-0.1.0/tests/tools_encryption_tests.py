from python.griddot.tools import rsa_generate, rsa_encrypt, rsa_decrypt


def test_encryption_decryption():
    private_key, public_key = rsa_generate()

    original_text = "Hello, GridDot!"
    encrypted_text = rsa_encrypt(public_key, original_text)
    assert encrypted_text != original_text  # Ensure encryption changed the text

    decrypted_text = rsa_decrypt(private_key, encrypted_text)
    assert decrypted_text == original_text  # Ensure decryption returns the original text
