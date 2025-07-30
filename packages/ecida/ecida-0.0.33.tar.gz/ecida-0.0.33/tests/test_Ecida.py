from Ecida import convert_to_dns_name


def test_convert_to_dns_name():
    test_cases = [
        ("My Example String!", "my-example-string"),
        ("ABC123", "abc123"),
        ("!@#$%^&*()_+=", ValueError),
        ("   leading-trailing-spaces   ", "leading-trailing-spaces"),
        ("special_characters!!!", "special-characters"),
        ("---multiple----hyphens---", "multiple-hyphens"),
        ("", ValueError),
    ]

    for string, expected_result in test_cases:
        try:
            result = convert_to_dns_name(string)
            assert result == expected_result
            print(f"PASS: {string} -> {result}")
        except ValueError:
            if expected_result is ValueError:
                print(f"PASS: {string} -> ValueError")
            else:
                print(
                    f"FAIL: {string} -> Expected: {expected_result}, Actual: ValueError"
                )
        except AssertionError:
            print(f"FAIL: {string} -> Expected: {expected_result}, Actual: {result}")


if __name__ == "__main__":
    test_convert_to_dns_name()
