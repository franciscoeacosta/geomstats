"""Unit tests for the Siegel manifold."""

import geomstats.backend as gs
import tests.conftest
from geomstats.geometry.lower_triangular_matrices import LowerTriangularMatrices
from geomstats.geometry.positive_lower_triangular_matrices import (
    PositiveLowerTriangularMatrices,
)
from geomstats.geometry.siegel import Siegel
from tests.conftest import Parametrizer
from tests.data.siegel_data import SiegelMetricTestData, SiegelTestData
from tests.geometry_test_cases import ComplexRiemannianMetricTestCase, OpenSetTestCase

CDTYPE = gs.get_default_cdtype()


class TestSiegel(OpenSetTestCase, metaclass=Parametrizer):
    """Test of Siegel methods."""

    testing_data = SiegelTestData()

    def test_belongs(self, n, mat, expected):
        self.assertAllClose(
            self.Space(n).belongs(gs.cast(gs.array(mat), dtype=CDTYPE)), expected
        )

    def test_projection(self, n, mat, expected):
        self.assertAllClose(
            self.Space(n).projection(gs.cast(gs.array(mat), dtype=CDTYPE)),
            gs.cast(gs.array(expected), dtype=CDTYPE),
        )

    def test_logm(self, mat, expected):
        self.assertAllClose(
            self.Space.logm(gs.cast(gs.array(mat), dtype=CDTYPE)),
            gs.cast(gs.array(expected), dtype=CDTYPE),
        )

    def test_cholesky_factor(self, n, mat, expected):
        result = self.Space.cholesky_factor(gs.cast(gs.array(mat), dtype=CDTYPE))

        self.assertAllClose(result, gs.cast(gs.array(expected), dtype=CDTYPE))
        self.assertTrue(gs.all(PositiveLowerTriangularMatrices(n).belongs(result)))

    def test_differential_cholesky_factor(self, n, tangent_vec, base_point, expected):
        result = self.Space.differential_cholesky_factor(
            gs.cast(gs.array(tangent_vec), dtype=CDTYPE),
            gs.cast(gs.array(base_point), dtype=CDTYPE),
        )
        self.assertAllClose(result, gs.cast(gs.array(expected), dtype=CDTYPE))
        self.assertTrue(gs.all(LowerTriangularMatrices(n).belongs(result)))

    def test_differential_power(self, power, tangent_vec, base_point, expected):
        result = self.Space.differential_power(
            power,
            gs.cast(gs.array(tangent_vec), dtype=CDTYPE),
            gs.cast(gs.array(base_point), dtype=CDTYPE),
        )
        self.assertAllClose(result, gs.cast(gs.array(expected), dtype=CDTYPE))

    def test_inverse_differential_power(self, power, tangent_vec, base_point, expected):
        result = self.Space.inverse_differential_power(
            power,
            gs.cast(gs.array(tangent_vec), dtype=CDTYPE),
            gs.cast(gs.array(base_point), dtype=CDTYPE),
        )
        self.assertAllClose(result, gs.cast(gs.array(expected), dtype=CDTYPE))

    def test_differential_log(self, tangent_vec, base_point, expected):
        result = self.Space.differential_log(
            gs.cast(gs.array(tangent_vec), dtype=CDTYPE),
            gs.cast(gs.array(base_point), dtype=CDTYPE),
        )
        self.assertAllClose(result, gs.cast(gs.array(expected), dtype=CDTYPE))

    def test_inverse_differential_log(self, tangent_vec, base_point, expected):
        result = self.Space.inverse_differential_log(
            gs.cast(gs.array(tangent_vec), dtype=CDTYPE),
            gs.cast(gs.array(base_point), dtype=CDTYPE),
        )
        self.assertAllClose(result, gs.cast(gs.array(expected), dtype=CDTYPE))

    def test_differential_exp(self, tangent_vec, base_point, expected):
        result = self.Space.differential_exp(
            gs.cast(gs.array(tangent_vec), dtype=CDTYPE),
            gs.cast(gs.array(base_point), dtype=CDTYPE),
        )
        self.assertAllClose(result, gs.cast(gs.array(expected), dtype=CDTYPE))

    def test_inverse_differential_exp(self, tangent_vec, base_point, expected):
        result = self.Space.inverse_differential_exp(
            gs.cast(gs.array(tangent_vec), dtype=CDTYPE),
            gs.cast(gs.array(base_point), dtype=CDTYPE),
        )
        self.assertAllClose(result, gs.cast(gs.array(expected), dtype=CDTYPE))

    def test_cholesky_factor_belongs(self, n, mat):
        result = self.Space(n).cholesky_factor(gs.cast(gs.array(mat), dtype=CDTYPE))
        self.assertAllClose(
            gs.all(PositiveLowerTriangularMatrices(n).belongs(result)), True
        )


class TestSiegelMetric(ComplexRiemannianMetricTestCase, metaclass=Parametrizer):
    skip_test_parallel_transport_ivp_is_isometry = True
    skip_test_parallel_transport_bvp_is_isometry = True
    skip_test_exp_geodesic_ivp = True
    skip_test_exp_ladder_parallel_transport = True
    skip_test_geodesic_ivp_belongs = True
    skip_test_covariant_riemann_tensor_is_skew_symmetric_1 = True
    skip_test_covariant_riemann_tensor_is_skew_symmetric_2 = True
    skip_test_covariant_riemann_tensor_bianchi_identity = True
    skip_test_covariant_riemann_tensor_is_interchange_symmetric = True
    skip_test_inner_product_is_symmetric = True
    skip_test_riemann_tensor_shape = True
    skip_test_scalar_curvature_shape = True
    skip_test_ricci_tensor_shape = True
    skip_test_sectional_curvature_shape = True

    testing_data = SiegelMetricTestData()

    def test_inner_product(
        self, n, power_affine, tangent_vec_a, tangent_vec_b, base_point, expected
    ):
        metric = self.Metric(n, power_affine)
        result = metric.inner_product(
            gs.cast(gs.array(tangent_vec_a), dtype=CDTYPE),
            gs.cast(gs.array(tangent_vec_b), dtype=CDTYPE),
            gs.cast(gs.array(base_point), dtype=CDTYPE),
        )
        self.assertAllClose(result, expected)

    def test_exp(self, n, power_affine, tangent_vec, base_point, expected):
        metric = self.Metric(n, power_affine)
        self.assertAllClose(
            metric.exp(
                gs.cast(gs.array(tangent_vec), dtype=CDTYPE),
                gs.cast(gs.array(base_point), dtype=CDTYPE),
            ),
            gs.cast(gs.array(expected), dtype=CDTYPE),
        )

    def test_log(self, n, power_affine, point, base_point, expected):
        metric = self.Metric(n, power_affine)
        self.assertAllClose(
            metric.log(
                gs.cast(gs.array(point), dtype=CDTYPE),
                gs.cast(gs.array(base_point), dtype=CDTYPE),
            ),
            gs.cast(gs.array(expected), dtype=CDTYPE),
        )
