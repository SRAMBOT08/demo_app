import React from 'react';
import { Link } from 'react-router-dom';
import { FiFacebook, FiTwitter, FiInstagram, FiLinkedin, FiMail, FiPhone, FiMapPin } from 'react-icons/fi';

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* About */}
          <div>
            <h3 className="text-white text-lg font-bold mb-4">
              <span className="text-primary-400">Quick</span>
              <span className="text-secondary-400">Court</span>
            </h3>
            <p className="text-sm mb-4">
              Your ultimate platform for booking sports facilities and connecting with players.
              Play more, worry less.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="hover:text-primary-400 transition">
                <FiFacebook className="w-5 h-5" />
              </a>
              <a href="#" className="hover:text-primary-400 transition">
                <FiTwitter className="w-5 h-5" />
              </a>
              <a href="#" className="hover:text-primary-400 transition">
                <FiInstagram className="w-5 h-5" />
              </a>
              <a href="#" className="hover:text-primary-400 transition">
                <FiLinkedin className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/facilities" className="hover:text-primary-400 transition">
                  Browse Facilities
                </Link>
              </li>
              <li>
                <Link to="/matches" className="hover:text-primary-400 transition">
                  Find Matches
                </Link>
              </li>
              <li>
                <Link to="/about" className="hover:text-primary-400 transition">
                  About Us
                </Link>
              </li>
              <li>
                <Link to="/contact" className="hover:text-primary-400 transition">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* For Owners */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">For Owners</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/owner/register" className="hover:text-primary-400 transition">
                  List Your Facility
                </Link>
              </li>
              <li>
                <Link to="/owner/dashboard" className="hover:text-primary-400 transition">
                  Owner Dashboard
                </Link>
              </li>
              <li>
                <Link to="/pricing" className="hover:text-primary-400 transition">
                  Pricing Plans
                </Link>
              </li>
              <li>
                <Link to="/faq" className="hover:text-primary-400 transition">
                  FAQ
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-white text-lg font-semibold mb-4">Contact Us</h3>
            <ul className="space-y-3 text-sm">
              <li className="flex items-start">
                <FiMapPin className="w-5 h-5 mr-2 mt-0.5 flex-shrink-0" />
                <span>123 Sports Avenue, City, State 12345</span>
              </li>
              <li className="flex items-center">
                <FiPhone className="w-5 h-5 mr-2 flex-shrink-0" />
                <span>+1 (555) 123-4567</span>
              </li>
              <li className="flex items-center">
                <FiMail className="w-5 h-5 mr-2 flex-shrink-0" />
                <span>support@quickcourt.com</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center text-sm">
          <p>&copy; {new Date().getFullYear()} QuickCourt. All rights reserved.</p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <Link to="/privacy" className="hover:text-primary-400 transition">
              Privacy Policy
            </Link>
            <Link to="/terms" className="hover:text-primary-400 transition">
              Terms of Service
            </Link>
            <Link to="/cookies" className="hover:text-primary-400 transition">
              Cookie Policy
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
