use crate::{small_linalg::Vector2, PhysicsQuantity};
use std::ops::{Add, Div, Index, IndexMut, Mul, Neg, Sub};
use crate::small_linalg::{Matrix2, Matrix2x3, Matrix3, Vector3};

#[derive(Clone, Copy, PartialEq, Debug)]
pub struct Matrix3x2<T: PhysicsQuantity> {
    pub data: [[T; 2]; 3],
}

impl<T: PhysicsQuantity> Matrix3x2<T> {
    pub fn new(data: [[T; 2]; 3]) -> Self {
        Self { data }
    }

    pub fn from_f64(data: [[f64; 2]; 3]) -> Self {
        let mut converted = [[<T as PhysicsQuantity>::zero(); 2]; 3];
        for i in 0..3 {
            for j in 0..2 {
                converted[i][j] = T::from_raw(data[i][j]);
            }
        }
        Self::new(converted)
    }

    pub fn as_f64(&self) -> Matrix3x2<f64> {
        Matrix3x2::new([
            [self.data[0][0].as_f64(), self.data[0][1].as_f64()],
            [self.data[1][0].as_f64(), self.data[1][1].as_f64()],
            [self.data[2][0].as_f64(), self.data[2][1].as_f64()],
        ])
    }

    pub fn transpose(&self) -> super::matrix2x3::Matrix2x3<T> {
        super::matrix2x3::Matrix2x3::new([
            [self.data[0][0], self.data[1][0], self.data[2][0]],
            [self.data[0][1], self.data[1][1], self.data[2][1]],
        ])
    }

    pub fn row(&self, i: usize) -> Vector2<T> {
        assert!(i < 3);
        Vector2::new(self.data[i])
    }
}

impl<T: PhysicsQuantity + Neg<Output = T>> Neg for Matrix3x2<T> {
    type Output = Self;
    fn neg(self) -> Self {
        Self::new([
            [-self.data[0][0], -self.data[0][1]],
            [-self.data[1][0], -self.data[1][1]],
            [-self.data[2][0], -self.data[2][1]],
        ])
    }
}

impl<T: PhysicsQuantity + Add<Output = T>> Add for Matrix3x2<T> {
    type Output = Self;
    fn add(self, rhs: Self) -> Self {
        let mut out = [[<T as PhysicsQuantity>::zero(); 2]; 3];
        for i in 0..3 {
            for j in 0..2 {
                out[i][j] = self.data[i][j] + rhs.data[i][j];
            }
        }
        Self::new(out)
    }
}

impl<T: PhysicsQuantity + Sub<Output = T>> Sub for Matrix3x2<T> {
    type Output = Self;
    fn sub(self, rhs: Self) -> Self {
        let mut out = [[<T as PhysicsQuantity>::zero(); 2]; 3];
        for i in 0..3 {
            for j in 0..2 {
                out[i][j] = self.data[i][j] - rhs.data[i][j];
            }
        }
        Self::new(out)
    }
}

impl<T: PhysicsQuantity> Index<(usize, usize)> for Matrix3x2<T> {
    type Output = T;
    fn index(&self, idx: (usize, usize)) -> &Self::Output {
        &self.data[idx.0][idx.1]
    }
}

impl<T: PhysicsQuantity> IndexMut<(usize, usize)> for Matrix3x2<T> {
    fn index_mut(&mut self, idx: (usize, usize)) -> &mut Self::Output {
        &mut self.data[idx.0][idx.1]
    }
}

impl<T: PhysicsQuantity> Matrix3x2<T> {
    pub fn dot_vector2<U, V>(&self, vec: &Vector2<U>) -> Vector3<V>
    where
        U: PhysicsQuantity,
        V: PhysicsQuantity + Add<Output = V>,
        T: Mul<U, Output = V>,
    {
        let r0 = self.data[0][0] * vec[0] + self.data[0][1] * vec[1];
        let r1 = self.data[1][0] * vec[0] + self.data[1][1] * vec[1];
        let r2 = self.data[2][0] * vec[0] + self.data[2][1] * vec[1];
        Vector3::new([r0, r1, r2])
    }
}


impl<T, U, V> Mul<Vector2<U>> for Matrix3x2<T>
where
    T: PhysicsQuantity + Mul<U, Output = V>,
    U: PhysicsQuantity,
    V: PhysicsQuantity + Add<Output = V>,
{
    type Output = Vector3<V>;

    fn mul(self, rhs: Vector2<U>) -> Self::Output {
        self.dot_vector2(&rhs)
    }
}

impl<T, U, V> Mul<Matrix3x2<U>> for Matrix3<T>
where
    T: PhysicsQuantity + Mul<U, Output = V>,
    U: PhysicsQuantity,
    V: PhysicsQuantity + Add<Output = V>,
{
    type Output = Matrix3x2<V>;

    fn mul(self, rhs: Matrix3x2<U>) -> Self::Output {
        let mut result = [[<V as num_traits::Zero>::zero(); 2]; 3];
        for i in 0..3 {
            for j in 0..2 {
                result[i][j] =
                    self[(i, 0)] * rhs[(0, j)] + self[(i, 1)] * rhs[(1, j)] + self[(i, 2)] * rhs[(2, j)];
            }
        }
        Matrix3x2::new(result)
    }
}


impl<T, U, V> Mul<Matrix2x3<U>> for Matrix3x2<T>
where
    T: PhysicsQuantity + Mul<U, Output = V>,
    U: PhysicsQuantity,
    V: PhysicsQuantity + Add<Output = V>,
{
    type Output = Matrix3<V>;

    fn mul(self, rhs: Matrix2x3<U>) -> Self::Output {
        let mut result = [[<V as num_traits::Zero>::zero(); 3]; 3];
        for i in 0..3 {
            for j in 0..3 {
                result[i][j] = self[(i, 0)] * rhs[(0, j)] + self[(i, 1)] * rhs[(1, j)];
            }
        }
        Matrix3::new(result)
    }
}

impl<T> Matrix3x2<T>
where
    T: PhysicsQuantity
    + Mul<T, Output = T>
    + Add<T, Output = T>
    + Sub<T, Output = T>
    + Div<T, Output = T>
    + Copy,
{
    pub fn pseudoinverse(&self) -> Option<Matrix2x3<T>> {
        let a_t = self.transpose();
        let at_a = a_t * *self;
        let at_a_inv = at_a.inverse()?;
        Some(at_a_inv * a_t)
    }
}

impl<T, U, V> Mul<Matrix2<U>> for Matrix3x2<T>
where
    T: PhysicsQuantity + Mul<U, Output = V>,
    U: PhysicsQuantity,
    V: PhysicsQuantity + Add<Output = V>,
{
    type Output = Matrix3x2<V>;

    fn mul(self, rhs: Matrix2<U>) -> Self::Output {
        let mut result = [[<V as PhysicsQuantity>::zero(); 2]; 3];
        for i in 0..3 {
            for j in 0..2 {
                result[i][j] = self[(i, 0)] * rhs[(0, j)] + self[(i, 1)] * rhs[(1, j)];
            }
        }
        Matrix3x2::new(result)
    }
}