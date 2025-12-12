import React from 'react';
import { Link } from 'react-router-dom';
import { 
  FiSearch, 
  FiCalendar, 
  FiUsers, 
  FiStar, 
  FiMapPin, 
  FiTrendingUp,
  FiShield,
  FiClock
} from 'react-icons/fi';

const LandingPage = () => {
  const features = [
    {
      icon: <FiSearch className="w-8 h-8" />,
      title: 'Easy Search',
      description: 'Find the perfect sports facility near you with advanced filters'
    },
    {
      icon: <FiCalendar className="w-8 h-8" />,
      title: 'Instant Booking',
      description: 'Book your favorite court in seconds with real-time availability'
    },
    {
      icon: <FiUsers className="w-8 h-8" />,
      title: 'Match-Making',
      description: 'Join or create matches and connect with players of your skill level'
    },
    {
      icon: <FiStar className="w-8 h-8" />,
      title: 'Reviews & Ratings',
      description: 'Read authentic reviews and ratings from the community'
    },
    {
      icon: <FiShield className="w-8 h-8" />,
      title: 'Secure Payments',
      description: 'Safe and encrypted payment processing for peace of mind'
    },
    {
      icon: <FiTrendingUp className="w-8 h-8" />,
      title: 'Owner Analytics',
      description: 'Comprehensive dashboard for facility owners to track earnings'
    }
  ];

  const sports = [
    'Basketball', 'Tennis', 'Badminton', 'Football', 
    'Cricket', 'Swimming', 'Volleyball', 'Squash'
  ];

  const howItWorks = [
    {
      step: '1',
      title: 'Search Facilities',
      description: 'Browse sports facilities by location, sport type, and availability',
      icon: <FiSearch className="w-6 h-6" />
    },
    {
      step: '2',
      title: 'Select Time Slot',
      description: 'Choose your preferred date and time from available slots',
      icon: <FiClock className="w-6 h-6" />
    },
    {
      step: '3',
      title: 'Book & Play',
      description: 'Confirm your booking and get ready to play!',
      icon: <FiCalendar className="w-6 h-6" />
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary-600 via-primary-700 to-secondary-600 text-white">
        <div className="absolute inset-0 bg-black opacity-10"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold mb-6 animate-fade-in">
              Book Sports Facilities <br />
              <span className="text-secondary-200">Anytime, Anywhere</span>
            </h1>
            <p className="text-xl md:text-2xl mb-8 text-primary-100 max-w-3xl mx-auto">
              Find and book the best sports facilities in your area. Join matches, connect with players, and elevate your game.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/facilities"
                className="bg-white text-primary-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition shadow-lg"
              >
                Browse Facilities
              </Link>
              <Link
                to="/register"
                className="bg-secondary-600 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-secondary-700 transition shadow-lg"
              >
                Get Started Free
              </Link>
            </div>
          </div>

          {/* Search Bar */}
          <div className="mt-12 max-w-4xl mx-auto">
            <div className="bg-white rounded-lg shadow-2xl p-4 flex flex-col md:flex-row gap-4">
              <div className="flex-1 relative">
                <FiMapPin className="absolute left-3 top-3.5 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  placeholder="Enter location..."
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 text-gray-900"
                />
              </div>
              <div className="flex-1">
                <select className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 text-gray-900">
                  <option value="">Select Sport</option>
                  {sports.map((sport) => (
                    <option key={sport} value={sport.toLowerCase()}>
                      {sport}
                    </option>
                  ))}
                </select>
              </div>
              <Link
                to="/facilities"
                className="bg-primary-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary-700 transition flex items-center justify-center"
              >
                <FiSearch className="mr-2" />
                Search
              </Link>
            </div>
          </div>
        </div>

        {/* Wave Divider */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320">
            <path
              fill="#ffffff"
              fillOpacity="1"
              d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,112C672,96,768,96,864,112C960,128,1056,160,1152,160C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"
            ></path>
          </svg>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Why Choose QuickCourt?
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Everything you need to book, play, and connect with the sports community
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                className="bg-gradient-to-br from-gray-50 to-white p-6 rounded-xl shadow-md hover:shadow-xl transition-shadow"
              >
                <div className="text-primary-600 mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              How It Works
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Get started in three simple steps
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {howItWorks.map((item, index) => (
              <div key={index} className="relative">
                <div className="bg-white p-8 rounded-xl shadow-md text-center hover:shadow-xl transition-shadow">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 text-primary-600 rounded-full text-2xl font-bold mb-4">
                    {item.step}
                  </div>
                  <div className="text-primary-600 mb-4 flex justify-center">
                    {item.icon}
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    {item.title}
                  </h3>
                  <p className="text-gray-600">{item.description}</p>
                </div>
                {index < howItWorks.length - 1 && (
                  <div className="hidden md:block absolute top-1/2 -right-4 transform -translate-y-1/2">
                    <svg
                      className="w-8 h-8 text-primary-300"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 bg-primary-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl md:text-5xl font-bold mb-2">500+</div>
              <div className="text-primary-100">Facilities</div>
            </div>
            <div>
              <div className="text-4xl md:text-5xl font-bold mb-2">10K+</div>
              <div className="text-primary-100">Active Users</div>
            </div>
            <div>
              <div className="text-4xl md:text-5xl font-bold mb-2">50K+</div>
              <div className="text-primary-100">Bookings Made</div>
            </div>
            <div>
              <div className="text-4xl md:text-5xl font-bold mb-2">4.8</div>
              <div className="text-primary-100">Average Rating</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-secondary-600 to-primary-600 text-white">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Get Started?
          </h2>
          <p className="text-xl mb-8 text-secondary-100">
            Join thousands of players and facility owners on QuickCourt today!
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/register"
              className="bg-white text-primary-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition shadow-lg"
            >
              Sign Up as Player
            </Link>
            <Link
              to="/owner/register"
              className="bg-secondary-700 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-secondary-800 transition shadow-lg border-2 border-white"
            >
              List Your Facility
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
