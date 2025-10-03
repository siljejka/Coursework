from exp_decay import ExponentialDecay


def test_exp_decay():
    """
    Checks that our ExponentialDecay class
    returns the correct value
    """

    a = 0.4
    u_t = 3.2
    ED = ExponentialDecay(a)
    u_d_t = ED(0,u_t)
    u_d_exp = -1.28

    tol = 1e-12
    msg = "ExponentialDecay returned unexpected value"

    assert (u_d_exp - u_d_t) < tol, msg



if __name__ == "__main__":
    test_exp_decay()
