import React from 'react';
import { Link } from 'react-router-dom';
import { FiMapPin, FiUsers, FiClock, FiCalendar } from 'react-icons/fi';
import { format } from 'date-fns';

const MatchCard = ({ match }) => {
  const {
    id,
    facility,
    date,
    start_time,
    end_time,
    sport_type,
    current_players,
    max_players,
    skill_level,
    created_by,
    is_public,
  } = match;

  // Calculate spots remaining
  const spotsRemaining = max_players - current_players;
  const isFull = spotsRemaining === 0;

  // Format date and time
  const formattedDate = date ? format(new Date(date), 'MMM dd, yyyy') : 'TBD';
  const timeSlot = `${start_time} - ${end_time}`;

  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 p-5">
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-xl font-bold text-gray-900 mb-1">
            {sport_type || 'Match'}
          </h3>
          <p className="text-sm text-gray-600">
            Hosted by {created_by?.name || 'Anonymous'}
          </p>
        </div>
        
        {/* Skill Level Badge */}
        {skill_level && (
          <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
            skill_level === 'beginner' 
              ? 'bg-green-100 text-green-800'
              : skill_level === 'intermediate'
              ? 'bg-blue-100 text-blue-800'
              : 'bg-purple-100 text-purple-800'
          }`}>
            {skill_level.charAt(0).toUpperCase() + skill_level.slice(1)}
          </span>
        )}
      </div>

      {/* Facility Info */}
      {facility && (
        <div className="flex items-start text-gray-600 mb-3">
          <FiMapPin className="w-4 h-4 mr-2 mt-1 flex-shrink-0" />
          <div className="text-sm">
            <p className="font-semibold text-gray-900">{facility.name}</p>
            <p className="text-xs">{facility.address}</p>
          </div>
        </div>
      )}

      {/* Date & Time */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        <div className="flex items-center text-gray-600">
          <FiCalendar className="w-4 h-4 mr-2 flex-shrink-0" />
          <span className="text-sm">{formattedDate}</span>
        </div>
        <div className="flex items-center text-gray-600">
          <FiClock className="w-4 h-4 mr-2 flex-shrink-0" />
          <span className="text-sm">{timeSlot}</span>
        </div>
      </div>

      {/* Players Count */}
      <div className="flex items-center justify-between mb-4 p-3 bg-gray-50 rounded-lg">
        <div className="flex items-center">
          <FiUsers className="w-5 h-5 text-primary-600 mr-2" />
          <span className="text-sm font-semibold text-gray-700">
            {current_players} / {max_players} Players
          </span>
        </div>
        <span className={`text-sm font-semibold ${
          isFull ? 'text-red-600' : 'text-green-600'
        }`}>
          {isFull ? 'Full' : `${spotsRemaining} spots left`}
        </span>
      </div>

      {/* Action Button */}
      <Link
        to={`/matches/${id}`}
        className={`block w-full text-center py-2 rounded-lg font-semibold transition ${
          isFull
            ? 'bg-gray-300 text-gray-600 cursor-not-allowed'
            : 'bg-primary-600 text-white hover:bg-primary-700'
        }`}
        onClick={(e) => isFull && e.preventDefault()}
      >
        {isFull ? 'Match Full' : 'Join Match'}
      </Link>
    </div>
  );
};

export default MatchCard;
