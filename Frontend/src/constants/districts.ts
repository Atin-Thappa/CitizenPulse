const DELHI_DISTRICTS: Record<string, [number, number]> = {
  "North Delhi":      [28.7041, 77.1025],
  "South Delhi":      [28.5245, 77.2066],
  "East Delhi":       [28.6438, 77.2942],
  "West Delhi":       [28.6288, 77.0878],
  "Central Delhi":    [28.6506, 77.2303],
  "North West Delhi": [28.7356, 77.1141],
  "South West Delhi": [28.5921, 77.0460],
  "North East Delhi": [28.6700, 77.2900],
  "Shahdara":         [28.6700, 77.2900],
  "New Delhi":        [28.6139, 77.2090],
  "Rohini":           [28.7356, 77.1141],
  "Dwarka":           [28.5921, 77.0460],
  "Janakpuri":        [28.6288, 77.0878],
  "Saket":            [28.5245, 77.2066],
  "Lajpat Nagar":     [28.5700, 77.2373],
  "Karol Bagh":       [28.6514, 77.1907],
  "Pitampura":        [28.7005, 77.1311],
  "Nehru Place":      [28.5491, 77.2518],
  "Okhla":            [28.5357, 77.2710],
  "Connaught Place":  [28.6315, 77.2167],
}

const DISTRICT_OPTIONS = Object.keys(DELHI_DISTRICTS)

export {DELHI_DISTRICTS, DISTRICT_OPTIONS}