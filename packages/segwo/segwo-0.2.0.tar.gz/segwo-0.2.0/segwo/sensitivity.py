r"""
Sensitivity curves
==================

This package provides functions to compute sensitivity curves from noise and
signal covariance matrices.

We generalize the definition of the sensitivity, sometimes called the combined
or optimal sensitivity, for a set of (potentially noise and signal) observables.
The sensitivity is defined as the trace of the product of the signal covariance
matrix (normalized by the strain power used to compute it, i.e., the trace of
the strain covariance matrix) and the inverse of the noise covariance matrix,

.. math::

    S(t, f) = \frac{1}{\text{Tr}[\mathbf{C}_\text{strain}]}
    \text{Tr}[\mathbf{C}_\text{signal}(t, f) \mathbf{C}_\text{noise}^{-1}(t,
    f)].

Note that the normalized signal covariance matrix is often interpreted as the
response matrix.

To compute single-channel sensitivity curves, one can trim the covariance
matrices to the single channel of interest. For example, if the signal
covariance matrix is of shape ``(..., N, N)`` and the noise covariance matrix
is of shape ``(..., M, M)``, one can compute the sensitivity for the first
channel of the signal covariance matrix and the first channel of the noise
covariance matrix as follows:

.. code-block:: python

    import numpy as np
    from segwo.sensitivity import compute_sensitivity_from_covariances

    sensitivity = compute_sensitivity_from_covariances(
        noise_cov[..., 0:1, 0:1], signal_cov[..., 0:1, 0:1], strain_power
    )

Note that the sum of single-channel sensitivities is not equal to the combined
sensitivity in general.

Computing sensitivity
---------------------

.. autofunction:: compute_sensitivity_from_covariances

"""

import numpy as np


def compute_sensitivity_from_covariances(
    noise_cov: np.ndarray, signal_cov: np.ndarray, strain_power: float = 1
) -> np.ndarray:
    r"""Compute sensitivity curve from noise and signal covariance matrices.

    The sensitivity is define as the trace of the product of the signal
    covariance matrix (normalized by the strain power used to compute it, i.e.,
    the trace of the strain covariance matrix) and the inverse of the noise
    covariance matrix,

    .. math::

        S(t, f) = \frac{1}{\text{Tr}[\mathbf{C}_\text{strain}]}
        \text{Tr}[\mathbf{C}_\text{signal}(t, f) \mathbf{C}_\text{noise}^{-1}(t,
        f)].

    Note that the normalized signal covariance matrix is often interpreted as
    the response matrix, and the sensitivity is defined as the trace of the
    product of the response and the inverse of the noise covariance matrix.

    This definition is valid for any set of :math:`N` observables for which the
    product :math:`\mathbf{C}_\text{signal} \mathbf{C}_\text{noise}^{-1}` is
    full rank.

    Args:
        noise_cov: Noise covariance matrix, of shape ``(..., N, N)``.
        signal_cov: Signal covariance matrix, of shape ``(..., N, N)``.
        strain_power: Strain power used to compute the signal covariance matrix,
            i.e., the trace of the strain covariance matrix. This is used to
            normalized the signal covariance matrix.

    Returns:
        Sensitivity curve, as an array of shape ``(...)``. Those axes are
        usually reserved for time and frequency.

        Units are those of ``response_cov`` divided by those of ``noise_cov``
        and power spectral density [1/Hz].

    Raises:
        ValueError: If the noise covariance matrix is singular.
    """
    if noise_cov.ndim < 2:
        raise ValueError("Noise covariance must have at least two dimensions.")
    if noise_cov.shape[-1] != noise_cov.shape[-2]:
        raise ValueError("Noise covariance must be square.")
    if signal_cov.ndim < 2:
        raise ValueError("Response covariance must have at least two dimensions.")
    if signal_cov.shape[-1] != signal_cov.shape[-2]:
        raise ValueError("Response covariance must be square.")

    if noise_cov.shape[1] == 1:
        inv_noise_cov = 1 / noise_cov
    else:
        try:
            inv_noise_cov = np.linalg.inv(noise_cov)  # (..., N, N)
        except np.linalg.LinAlgError as e:
            raise ValueError("Noise covariance is singular.") from e

    snr_psd = np.einsum("...ij, ...ji -> ...", signal_cov, inv_noise_cov)  # (...)
    np.allclose(snr_psd.imag / np.abs(snr_psd), 0)  # imaginary part should be small

    normalized_snr_psd = snr_psd.real / strain_power
    return 1 / normalized_snr_psd
