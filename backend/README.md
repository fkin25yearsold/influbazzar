# Influbazzar Backend API

A comprehensive FastAPI backend for a three-sided influencer collaboration marketplace platform.

## 🚀 Features

### Multi-Role Authentication System
- **Creators** - Influencers who apply to campaigns and earn money
- **Brands** - Businesses who run influencer campaigns  
- **Agencies** - Firms that manage multiple creators and/or brands

### Core Functionality
- JWT-based authentication with role-based access control
- Email verification with OTP system
- Google OAuth integration
- Complete profile management for all user types
- Advanced discovery and search functionality
- Comprehensive onboarding flow

## 🏗️ Architecture

### Database Models
- **User** - Base user model with role and onboarding status
- **CreatorProfile** - Detailed creator information, metrics, and portfolio
- **BrandProfile** - Brand information, campaign preferences, and budget
- **AgencyProfile** - Agency details, team management, and performance metrics

### API Structure