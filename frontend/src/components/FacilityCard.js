import React from 'react';
import { Link } from 'react-router-dom';
import { FiMapPin, FiStar, FiClock, FiDollarSign } from 'react-icons/fi';

const FacilityCard = ({ facility }) => {
  const {
    id,
    name,
    address,
    sport_type,
    price_per_hour,
    images,
    average_rating,
    total_reviews,
    availability_status,
  } = facility;

  // Use first image or placeholder
  const imageUrl = images && images.length > 0 
    ? images[0] 
    : '/placeholder-facility.jpg';

  return (
    <Link
      to={`/facilities/${id}`}
      className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300"
    >
      {/* Image */}
      <div className="relative h-48 overflow-hidden">
        <img
          src={imageUrl}
          alt={name}
          className="w-full h-full object-cover hover:scale-110 transition-transform duration-300"
        />
        
        {/* Sport Type Badge */}
        <div className="absolute top-4 left-4">
          <span className="bg-primary-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
            {sport_type}
          </span>
        </div>

        {/* Availability Badge */}
        {availability_status && (
          <div className="absolute top-4 right-4">
            <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
              availability_status === 'available' 
                ? 'bg-green-500 text-white' 
                : 'bg-red-500 text-white'
            }`}>
              {availability_status === 'available' ? 'Available' : 'Booked'}
            </span>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-4">
        {/* Title */}
        <h3 className="text-xl font-bold text-gray-900 mb-2 line-clamp-1">
          {name}
        </h3>

        {/* Location */}
        <div className="flex items-start text-gray-600 mb-3">
          <FiMapPin className="w-4 h-4 mr-2 mt-1 flex-shrink-0" />
          <span className="text-sm line-clamp-2">{address}</span>
        </div>

        {/* Rating */}
        <div className="flex items-center mb-3">
          <FiStar className="w-5 h-5 text-yellow-400 fill-current" />
          <span className="ml-1 text-gray-900 font-semibold">
            {average_rating ? average_rating.toFixed(1) : 'N/A'}
          </span>
          <span className="ml-1 text-gray-500 text-sm">
            ({total_reviews || 0} reviews)
          </span>
        </div>

        {/* Price */}
        <div className="flex items-center justify-between pt-3 border-t border-gray-200">
          <div className="flex items-center text-primary-600 font-bold text-lg">
            <FiDollarSign className="w-5 h-5" />
            <span>{price_per_hour}</span>
            <span className="text-gray-500 text-sm font-normal ml-1">/hour</span>
          </div>
          <button className="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition text-sm font-semibold">
            Book Now
          </button>
        </div>
      </div>
    </Link>
  );
};

export default FacilityCard;
