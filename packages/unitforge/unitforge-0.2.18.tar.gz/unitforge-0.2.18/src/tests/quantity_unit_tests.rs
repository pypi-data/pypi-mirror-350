#![cfg(test)]
mod tests {
    use crate::*;

    #[test]
    fn test_new() {
        let input = 1000;
        let output = Distance::new(input.into(), DistanceUnit::mm);
        assert_eq!(
            output,
            Distance {
                multiplier: 1000f64,
                power: -3
            }
        )
    }
}
