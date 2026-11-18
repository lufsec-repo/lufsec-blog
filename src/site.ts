// Central site settings — edit here to change branding, nav and CTAs.
// Styled to match www.lufsec.com (Thinkific theme).
export const SITE = {
  title: 'LufSec Blog',
  brand: 'LufSec',
  description: 'Your Hub for Cybersecurity Training & Research',
  url: 'https://blog.lufsec.com',
  author: 'Luciano Ferrari',
  logo: '/lufsec-logo.png',
  favicon: '/content/images/2025/08/1.png',
  heroImage: '/content/images/2026/06/hero-banner-lufsec-homepage.jpeg',
  ogImage: '/content/images/2026/06/hero-banner-lufsec-homepage.jpeg',
  gaId: 'G-LP6ZQYG2VZ',
  postsPerPage: 12,
};

// Same menu as lufsec.com
export const NAV = [
  { label: 'All Products', href: 'https://www.lufsec.com/collections' },
  { label: 'Blog', href: '/', current: true },
  { label: 'About', href: 'https://www.lufsec.com/pages/about' },
  { label: 'Contact Us', href: 'https://www.lufsec.com/pages/contact-us' },
  { label: 'Sign In', href: 'https://www.lufsec.com/users/sign_in' },
];

// Same footer as lufsec.com
export const FOOTER_LINKS = [
  { label: 'Privacy Policy', href: 'https://www.lufsec.com/pages/lufsec-privacy-policy' },
  { label: 'Terms', href: 'https://www.lufsec.com/pages/lufsec-terms' },
  { label: 'All Courses', href: 'https://www.lufsec.com/collections' },
  { label: 'RSS', href: '/rss.xml' },
];

export const SOCIAL = {
  youtube: 'https://youtube.com/lufsec',
  instagram: 'https://instagram.com/lufsec',
  linkedin: 'https://www.linkedin.com/company/lufsec',
};

// Course paths (same as "Choose Your Path" on lufsec.com)
export const PATHS = [
  { label: 'AI Security', href: 'https://www.lufsec.com/collections/ai-security' },
  { label: 'Car Hacking', href: 'https://www.lufsec.com/collections/car-hacking' },
  { label: 'IoT Hacking', href: 'https://www.lufsec.com/collections/iot-hacking' },
  { label: 'For Teams', href: 'https://www.lufsec.com/collections/for-teams' },
  { label: 'Free Resources', href: 'https://www.lufsec.com/collections/free-resources' },
];

// Shown at the end of every post
export const COURSE_CTA = {
  heading: 'Go hands-on with LufSec',
  text: 'Master ethical hacking and AI security with hands-on labs built for the future of cybersecurity.',
  points: ['Real-World Hacking Labs', 'Industry-Driven Curriculum', 'Automotive & AI Security Specialization', 'Certificate of Completion'],
  button: 'Explore All Courses',
  href: 'https://www.lufsec.com/collections',
};
