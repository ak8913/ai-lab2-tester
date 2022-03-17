"""
Tests solution program of CSCI-630 Lab 2 (2215)
"""

import glob
import subprocess


def load_expected():
    """
    Get the expected output for each file from the output file
    :return: dict['filename': 'expected-output']
    """
    with open('answers.out') as ans:
        expected = {}
        test_file = ans.readline().strip()
        while test_file:
            filename = test_file
            expected_out = ans.readline().strip()
            expected[filename] = expected_out
            test_file = ans.readline().strip()

    return expected


def print_summary(fails_collected, total_tests):
    """

    :param fails_collected:
    :return:
    """
    print("*" * 20 + "SUMMARY" + "*" * 20)
    if fails_collected:
        print("The program didn't give the expected output for "
              "the following files: \n")
        for fail in fails_collected:
            print("File: " + fail[0])
            print("Reason: " + fail[1])
            print()

    print("Tests passed: {}".format(total_tests - len(fails_collected)))
    print("Tests failed: {}".format(len(fails_collected)))

    if not fails_collected:
        print("Wohoo!")


def run_tests_on_files(directory, expected):
    """
    Run all test files in a directory
    :param directory:
    :param expected:
    :return:
    """

    cnf_files = glob.glob(directory + "/*.cnf")

    failed_for_files = []

    for cnf_file in cnf_files:
        try:
            expected_output = expected[cnf_file.split("/")[1].strip()]
            out = subprocess.check_output(["python3", "lab2.py", cnf_file])
            actual_output = out.decode("utf-8").strip()
            if not actual_output == expected_output:
                failed_for_files.append(
                    (cnf_file, "Wrong output (Expected: {}, got: {})".format(
                        expected_output, actual_output
                    ))
                )
        except subprocess.CalledProcessError as e:
            failed_for_files.append(
                (cnf_file, "Unexpected error")
            )

    return  failed_for_files


def run_tests():
    """
    Run tests on all the files
    :return:
    """

    expected = load_expected()

    fails_collected = []

    print("Testing files in constants/: ", end='  ')
    fails_collected.extend(
        run_tests_on_files("constants", expected)
    )
    print("done")

    print("Testing files in functions/: ", end='  ')
    fails_collected.extend(
        run_tests_on_files("functions", expected)
    )
    print("done")

    print("Testing files in prop/: ", end='  ')
    fails_collected.extend(
        run_tests_on_files("prop", expected)
    )
    print("done")

    print("Testing files in universals/: ", end='  ')
    fails_collected.extend(
        run_tests_on_files("universals", expected)
    )
    print("done")

    print("Testing files in universals+constants/: ", end='  ')
    fails_collected.extend(
        run_tests_on_files("universals+constants", expected)
    )
    print("done")

    print_summary(fails_collected, len(expected))


if __name__ == '__main__':
    run_tests()





