import React from 'react';
import { FiStar } from 'react-icons/fi';

const StarRating = ({ rating, maxRating = 5, size = 'md', onRatingChange, readonly = false }) => {
  const [hoverRating, setHoverRating] = React.useState(0);

  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-5 h-5',
    lg: 'w-6 h-6',
  };

  const handleClick = (value) => {
    if (!readonly && onRatingChange) {
      onRatingChange(value);
    }
  };

  return (
    <div className="flex items-center">
      {[...Array(maxRating)].map((_, index) => {
        const starValue = index + 1;
        const isFilled = starValue <= (hoverRating || rating);

        return (
          <button
            key={index}
            type="button"
            className={`${readonly ? 'cursor-default' : 'cursor-pointer'} transition`}
            onClick={() => handleClick(starValue)}
            onMouseEnter={() => !readonly && setHoverRating(starValue)}
            onMouseLeave={() => !readonly && setHoverRating(0)}
            disabled={readonly}
          >
            <FiStar
              className={`${sizeClasses[size]} ${
                isFilled
                  ? 'text-yellow-400 fill-current'
                  : 'text-gray-300'
              }`}
            />
          </button>
        );
      })}
    </div>
  );
};

export default StarRating;
