"""Unit tests for euclidean space module."""

import geomstats.backend as gs
import unittest

from geomstats.euclidean_space import EuclideanSpace


class TestEuclideanSpaceMethods(unittest.TestCase):
    _multiprocess_can_split_ = True

    def setUp(self):
        gs.random.seed(1234)

        self.dimension = 2
        self.space = EuclideanSpace(self.dimension)
        self.metric = self.space.metric

        self.n_samples = 10
        self.depth = 3

    def test_inner_product_matrix(self):
        result = self.metric.inner_product_matrix()

        expected = gs.eye(self.dimension)
        self.assertTrue(gs.allclose(result, expected))

    def test_inner_product(self):
        point_a = gs.array([0, 1])
        point_b = gs.array([2, 10])

        result = self.metric.inner_product(point_a, point_b)
        expected = gs.dot(point_a, point_b)
        self.assertTrue(gs.allclose(result, expected))

    def test_inner_product_vectorization(self):
        n_samples = self.n_samples
        one_point_a = self.space.random_uniform(n_samples=1)
        one_point_b = self.space.random_uniform(n_samples=1)
        n_points_a = self.space.random_uniform(n_samples=n_samples)
        n_points_b = self.space.random_uniform(n_samples=n_samples)

        result = self.metric.inner_product(one_point_a, one_point_b)
        expected = gs.dot(one_point_a, one_point_b.transpose())
        self.assertTrue(gs.allclose(result, expected))

        result = self.metric.inner_product(n_points_a, one_point_b)
        expected = gs.dot(n_points_a, one_point_b.transpose())
        self.assertTrue(gs.isclose(result.shape, n_samples),
                        'result.shape = {}'.format(result.shape))
        self.assertTrue(gs.allclose(result, expected),
                        'result = {}\n expected = {}'.format(result, expected))

        result = self.metric.inner_product(one_point_a, n_points_b)
        expected = gs.dot(one_point_a, n_points_b.transpose()).transpose()
        self.assertTrue(gs.isclose(result.shape, n_samples))
        self.assertTrue(gs.allclose(result, expected))

        result = self.metric.inner_product(n_points_a, n_points_b)
        expected = gs.zeros(n_samples)
        for i in range(n_samples):
            expected[i] = gs.dot(n_points_a[i], n_points_b[i])
        self.assertTrue(gs.isclose(result.shape, n_samples))
        self.assertTrue(gs.allclose(result, expected))

    def test_inner_product_vectorization_with_channels(self):
        n_samples = self.n_samples
        depth = self.depth

        one_point_a = self.space.random_uniform(n_samples=1,
                                                depth=depth)
        one_point_b = self.space.random_uniform(n_samples=1,
                                                depth=depth)
        n_points_a = self.space.random_uniform(n_samples=n_samples,
                                               depth=depth)
        n_points_b = self.space.random_uniform(n_samples=n_samples,
                                               depth=depth)

        result = self.metric.inner_product(one_point_a, one_point_b)
        expected = gs.einsum('...k,...k->...', one_point_a, one_point_b)
        self.assertTrue(
            gs.allclose(result, expected),
            'result = {} \n expected = {}'.format(result, expected))

        result = self.metric.inner_product(n_points_a, one_point_b)
        expected = gs.zeros((n_samples, depth,))
        for i in range(n_samples):
            for j in range(depth):
                expected[i, j] = gs.dot(n_points_a[i, j], one_point_b[j])
        self.assertTrue(gs.allclose(result.shape, (n_samples, depth)),
                        'result.shape = {}'.format(result.shape))
        self.assertTrue(gs.allclose(result, expected))

        result = self.metric.inner_product(one_point_a, n_points_b)
        expected = gs.zeros((n_samples, depth,))
        for i in range(n_samples):
            for j in range(depth):
                expected[i, j] = gs.dot(one_point_a[j], n_points_b[i, j])
        self.assertTrue(gs.allclose(result.shape, (n_samples, depth)))
        self.assertTrue(gs.allclose(result, expected))

        result = self.metric.inner_product(n_points_a, n_points_b)
        expected = gs.zeros((n_samples, depth,))
        for i in range(n_samples):
            for j in range(depth):
                expected[i, j] = gs.dot(n_points_a[i, j], n_points_b[i, j])
        self.assertTrue(gs.allclose(result.shape, (n_samples, depth)))
        self.assertTrue(gs.allclose(result, expected))

    def test_squared_norm(self):
        point = gs.array([-2, 4])

        result = self.metric.squared_norm(point)
        expected = gs.linalg.norm(point) ** 2
        self.assertTrue(gs.allclose(result, expected))

    def test_squared_norm_vectorization(self):
        n_samples = self.n_samples
        n_points = self.space.random_uniform(n_samples=n_samples)

        result = self.metric.squared_norm(n_points)
        expected = gs.linalg.norm(n_points, axis=1) ** 2
        self.assertTrue(gs.isclose(result.shape, n_samples))
        self.assertTrue(gs.allclose(result, expected))

    def test_squared_norm_vectorization_with_channels(self):
        n_samples = self.n_samples
        depth = self.depth
        n_points = self.space.random_uniform(n_samples=n_samples,
                                             depth=depth)

        result = self.metric.squared_norm(n_points)
        expected = gs.linalg.norm(n_points, axis=-1) ** 2
        self.assertTrue(gs.allclose(result.shape, (n_samples, depth)))
        self.assertTrue(gs.allclose(result, expected))

    def test_norm(self):
        point = gs.array([-2, 4])

        result = self.metric.norm(point)
        expected = gs.linalg.norm(point)
        self.assertTrue(gs.allclose(result, expected))

    def test_norm_vectorization(self):
        n_samples = self.n_samples
        n_points = self.space.random_uniform(n_samples=n_samples)

        result = self.metric.norm(n_points)
        expected = gs.linalg.norm(n_points, axis=1)
        self.assertTrue(gs.isclose(result.shape, n_samples))
        self.assertTrue(gs.allclose(result, expected),
                        '\n result = {}'
                        '\n expected = {}'.format(result, expected))

    def test_norm_vectorization_with_channels(self):
        n_samples = self.n_samples
        depth = self.depth
        n_points = self.space.random_uniform(n_samples=n_samples,
                                             depth=depth)

        result = self.metric.norm(n_points)
        expected = gs.linalg.norm(n_points, axis=-1)

        self.assertTrue(gs.allclose(result.shape, (n_samples, depth)))
        self.assertTrue(gs.allclose(result, expected),
                        '\n result = {}'
                        '\n expected = {}'.format(result, expected))

    def test_exp(self):
        base_point = gs.array([0, 1])
        vector = gs.array([2, 10])

        result = self.metric.exp(tangent_vec=vector,
                                 base_point=base_point)
        expected = base_point + vector
        self.assertTrue(gs.allclose(result, expected))

    def test_exp_vectorization(self):
        n_samples = self.n_samples
        dim = self.dimension
        one_tangent_vec = self.space.random_uniform(n_samples=1)
        one_base_point = self.space.random_uniform(n_samples=1)
        n_tangent_vecs = self.space.random_uniform(n_samples=n_samples)
        n_base_points = self.space.random_uniform(n_samples=n_samples)

        result = self.metric.exp(one_tangent_vec, one_base_point)
        expected = one_tangent_vec + one_base_point
        self.assertTrue(gs.allclose(result, expected))

        result = self.metric.exp(n_tangent_vecs, one_base_point)
        self.assertTrue(gs.allclose(result.shape, (n_samples, dim)),
                        '\n result.shape = {}'.format(result.shape))

        result = self.metric.exp(one_tangent_vec, n_base_points)
        self.assertTrue(gs.allclose(result.shape, (n_samples, dim)))

        result = self.metric.exp(n_tangent_vecs, n_base_points)
        self.assertTrue(gs.allclose(result.shape, (n_samples, dim)))

    def test_exp_vectorization_with_channels(self):
        n_samples = self.n_samples
        depth = self.depth

        dim = self.dimension
        one_tangent_vec = self.space.random_uniform(n_samples=1,
                                                    depth=depth)
        one_base_point = self.space.random_uniform(n_samples=1,
                                                   depth=depth)
        n_tangent_vecs = self.space.random_uniform(n_samples=n_samples,
                                                   depth=depth)
        n_base_points = self.space.random_uniform(n_samples=n_samples,
                                                  depth=depth)

        result = self.metric.exp(one_tangent_vec, one_base_point)
        expected = one_tangent_vec + one_base_point
        self.assertTrue(gs.allclose(result, expected))

        result = self.metric.exp(n_tangent_vecs, one_base_point)
        self.assertTrue(
            gs.allclose(result.shape, (n_samples, depth, dim)),
            '\n result.shape = {}'.format(result.shape))

        result = self.metric.exp(one_tangent_vec, n_base_points)
        self.assertTrue(
            gs.allclose(result.shape, (n_samples, depth, dim)))

        result = self.metric.exp(n_tangent_vecs, n_base_points)
        self.assertTrue(
            gs.allclose(result.shape, (n_samples, depth, dim)))

    def test_log(self):
        base_point = gs.array([0, 1])
        point = gs.array([2, 10])

        result = self.metric.log(point=point, base_point=base_point)
        expected = point - base_point
        self.assertTrue(gs.allclose(result, expected))

    def test_log_vectorization(self):
        n_samples = self.n_samples
        dim = self.dimension
        one_point = self.space.random_uniform(n_samples=1)
        one_base_point = self.space.random_uniform(n_samples=1)
        n_points = self.space.random_uniform(n_samples=n_samples)
        n_base_points = self.space.random_uniform(n_samples=n_samples)

        result = self.metric.log(one_point, one_base_point)
        expected = one_point - one_base_point
        self.assertTrue(gs.allclose(result, expected))

        result = self.metric.log(n_points, one_base_point)
        self.assertTrue(gs.allclose(result.shape, (n_samples, dim)))

        result = self.metric.log(one_point, n_base_points)
        self.assertTrue(gs.allclose(result.shape, (n_samples, dim)))

        result = self.metric.log(n_points, n_base_points)
        self.assertTrue(gs.allclose(result.shape, (n_samples, dim)))

    def test_log_vectorization_with_channels(self):
        n_samples = self.n_samples
        depth = self.depth

        dim = self.dimension
        one_point = self.space.random_uniform(n_samples=1,
                                              depth=depth)
        one_base_point = self.space.random_uniform(n_samples=1,
                                                   depth=depth)
        n_points = self.space.random_uniform(n_samples=n_samples,
                                             depth=depth)
        n_base_points = self.space.random_uniform(n_samples=n_samples,
                                                  depth=depth)

        result = self.metric.log(one_point, one_base_point)
        expected = one_point - one_base_point
        self.assertTrue(gs.allclose(result, expected))

        result = self.metric.log(n_points, one_base_point)
        self.assertTrue(
            gs.allclose(result.shape, (n_samples, depth, dim)))

        result = self.metric.log(one_point, n_base_points)
        self.assertTrue(
            gs.allclose(result.shape, (n_samples, depth, dim)))

        result = self.metric.log(n_points, n_base_points)
        self.assertTrue(
            gs.allclose(result.shape, (n_samples, depth, dim)))

    def test_squared_dist(self):
        point_a = gs.array([-1, 4])
        point_b = gs.array([1, 1])

        result = self.metric.squared_dist(point_a, point_b)
        vec = point_b - point_a
        expected = gs.dot(vec, vec)
        self.assertTrue(gs.allclose(result, expected))

    def test_squared_dist_vectorization(self):
        n_samples = self.n_samples
        one_point_a = self.space.random_uniform(n_samples=1)
        one_point_b = self.space.random_uniform(n_samples=1)
        n_points_a = self.space.random_uniform(n_samples=n_samples)
        n_points_b = self.space.random_uniform(n_samples=n_samples)

        result = self.metric.squared_dist(one_point_a, one_point_b)
        vec = one_point_a - one_point_b
        expected = gs.dot(vec, vec.transpose())
        self.assertTrue(gs.allclose(result, expected))

        result = self.metric.squared_dist(n_points_a, one_point_b)
        self.assertTrue(gs.isclose(result.shape, n_samples))

        result = self.metric.squared_dist(one_point_a, n_points_b)
        self.assertTrue(gs.isclose(result.shape, n_samples))

        result = self.metric.squared_dist(n_points_a, n_points_b)
        expected = gs.zeros(n_samples)
        for i in range(n_samples):
            vec = n_points_a[i] - n_points_b[i]
            expected[i] = gs.dot(vec, vec.transpose())
        self.assertTrue(gs.isclose(result.shape, n_samples))
        self.assertTrue(gs.allclose(result, expected))

    def test_dist(self):
        point_a = gs.array([0, 1])
        point_b = gs.array([2, 10])

        result = self.metric.dist(point_a, point_b)
        expected = gs.linalg.norm(point_b - point_a)
        self.assertTrue(gs.allclose(result, expected))

    def test_dist_vectorization(self):
        n_samples = self.n_samples
        one_point_a = self.space.random_uniform(n_samples=1)
        one_point_b = self.space.random_uniform(n_samples=1)
        n_points_a = self.space.random_uniform(n_samples=n_samples)
        n_points_b = self.space.random_uniform(n_samples=n_samples)

        result = self.metric.dist(one_point_a, one_point_b)
        vec = one_point_a - one_point_b
        expected = gs.sqrt(gs.dot(vec, vec.transpose()))
        self.assertTrue(gs.allclose(result, expected))

        result = self.metric.dist(n_points_a, one_point_b)
        self.assertTrue(gs.isclose(result.shape, n_samples))

        result = self.metric.dist(one_point_a, n_points_b)
        self.assertTrue(gs.isclose(result.shape, n_samples))

        result = self.metric.dist(n_points_a, n_points_b)
        expected = gs.zeros(n_samples)
        for i in range(n_samples):
            vec = n_points_a[i] - n_points_b[i]
            expected[i] = gs.sqrt(gs.dot(vec, vec.transpose()))
        self.assertTrue(gs.isclose(result.shape, n_samples))
        self.assertTrue(gs.allclose(result, expected))

    def test_random_uniform_and_belongs(self):
        point = self.space.random_uniform()
        self.assertTrue(self.space.belongs(point))

    def test_random_uniform_and_belongs_vectorization(self):
        n_samples = self.n_samples
        n_points = self.space.random_uniform(n_samples=n_samples)
        self.assertTrue(gs.all(self.space.belongs(n_points)))

    def test_geodesic_and_belongs(self):
        initial_point = self.space.random_uniform()
        initial_tangent_vec = gs.array([2., 0.])
        geodesic = self.metric.geodesic(
                                   initial_point=initial_point,
                                   initial_tangent_vec=initial_tangent_vec)

        t = gs.linspace(start=0, stop=1, num=100)
        points = geodesic(t)
        self.assertTrue(gs.all(self.space.belongs(points)))

    def test_mean(self):
        point = gs.array([1, 4])
        result = self.metric.mean(points=[point, point, point])
        expected = point

        self.assertTrue(gs.allclose(result, expected))

        points = gs.array([[1, 2],
                           [2, 3],
                           [3, 4],
                           [4, 5]])
        weights = gs.array([1, 2, 1, 2])

        result = self.metric.mean(points, weights)
        expected = gs.array([16., 22.]) / 6.
        self.assertTrue(gs.allclose(result, expected))

    def test_variance(self):
        points = gs.array([[1, 2],
                           [2, 3],
                           [3, 4],
                           [4, 5]])
        weights = gs.array([1, 2, 1, 2])
        base_point = gs.zeros(2)
        result = self.metric.variance(points, weights, base_point)
        # we expect the average of the points' sq norms.
        expected = (1 * 5. + 2 * 13. + 1 * 25. + 2 * 41.) / 6.
        self.assertTrue(gs.allclose(result, expected))


if __name__ == '__main__':
        unittest.main()
