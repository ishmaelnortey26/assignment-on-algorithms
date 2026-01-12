import pytest

from algorithms_files.rsa_encryption import (
    generate_rsa_keys,
    rsa_encrypt_message,
    rsa_decrypt_message,
    validate_public_key,
    validate_private_key,
)


def test_key_generation_returns_two_keys():
    public_key, private_key = generate_rsa_keys(bits=16)

    assert isinstance(public_key, tuple) and len(public_key) == 2
    assert isinstance(private_key, tuple) and len(private_key) == 2

    e, n1 = public_key
    d, n2 = private_key

    assert isinstance(e, int) and isinstance(n1, int)
    assert isinstance(d, int) and isinstance(n2, int)
    assert n1 == n2  # both keys must share the same modulus n


def test_encrypt_decrypt_roundtrip_simple_message():
    public_key, private_key = generate_rsa_keys(bits=16)

    message = "hello RSA!"
    cipher = rsa_encrypt_message(message, public_key)
    plain = rsa_decrypt_message(cipher, private_key)

    assert plain == message
    assert isinstance(cipher, list)
    assert all(isinstance(x, int) for x in cipher)


def test_encrypt_decrypt_roundtrip_with_unicode():
    public_key, private_key = generate_rsa_keys(bits=16)

    message = "Hello 👋🏽"
    cipher = rsa_encrypt_message(message, public_key)
    plain = rsa_decrypt_message(cipher, private_key)

    assert plain == message


def test_encrypt_empty_string():
    public_key, private_key = generate_rsa_keys(bits=16)

    message = ""
    cipher = rsa_encrypt_message(message, public_key)
    plain = rsa_decrypt_message(cipher, private_key)

    assert cipher == []
    assert plain == ""


def test_encrypt_none_raises():
    public_key, _ = generate_rsa_keys(bits=16)

    with pytest.raises(ValueError):
        rsa_encrypt_message(None, public_key)


def test_decrypt_none_raises():
    _, private_key = generate_rsa_keys(bits=16)

    with pytest.raises(ValueError):
        rsa_decrypt_message(None, private_key)


def test_public_key_validation_rejects_small_modulus():
    # n <= 255 should be rejected
    with pytest.raises(ValueError):
        validate_public_key((3, 255))

    with pytest.raises(ValueError):
        validate_public_key((3, 200))


def test_private_key_validation_rejects_small_modulus():
    with pytest.raises(ValueError):
        validate_private_key((3, 255))

    with pytest.raises(ValueError):
        validate_private_key((3, 100))


def test_user_provided_keys_work():
    # "user provided keys" = we generated them once, then passed them in
    public_key, private_key = generate_rsa_keys(bits=16)

    message = "user keys"
    cipher = rsa_encrypt_message(message, public_key)
    plain = rsa_decrypt_message(cipher, private_key)

    assert plain == message