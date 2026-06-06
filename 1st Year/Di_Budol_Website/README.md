# Di-Budol: Digital Literacy & Online Safety Educational Platform

**Di-Budol** is a comprehensive web-based educational platform dedicated to promoting digital literacy and online safety awareness. The platform provides accessible resources, tutorials, and support materials designed to empower individuals and communities, with a particular focus on advocating for orphan welfare and vulnerable populations in the Philippines.

---

## Project Overview

Di-Budol addresses the critical gap in digital literacy education by providing:
- Educational content on digital safety and online security
- Community resources and support for at-risk populations
- Accessible learning materials for diverse audiences
- Advocacy for orphan welfare and social responsibility

The platform serves as both an informational hub and a gateway for community engagement, featuring multiple educational sections and direct support channels.

---

## Key Features

### Homepage
- **Digital Literacy Introduction**: Foundational concepts and importance of digital skills
- **Cyber Safety Awareness**: Essential tips for protecting personal information online
- **Community Engagement**: Call-to-action buttons for user involvement
- **Responsive Design**: Optimized viewing experience across all devices

### Learning Center
- **Video Tutorials**: Curated collection of educational videos covering:
  - Introduction to Digital Literacy
  - Identifying and Avoiding Scam Emails
  - Social Media Safety Best Practices
  - Secure Password Management
  - And more...
- **Interactive Learning Materials**: Guides, printable resources, and exercises
- **Community Session Resources**: Materials designed for group learning and workshops
- **Progressive Skill Building**: Content organized from beginner to advanced levels

### Support Section
- **Counseling Services**: Information and access to mental health support
- **Community Resources**: Local assistance and referral information
- **Crisis Support**: 24/7 contact channels for urgent needs
- **Educational Support**: Mentoring and academic assistance resources

### Contact & Engagement
- **24/7 Contact Line**: Always-available communication channel
- **Donation Integration**: Seamless connection to supporting causes
- **Multi-platform Support**: Multiple ways to get involved and contribute

---

## Technical Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | HTML5, CSS3 |
| **Styling** | CSS3 with Responsive Design |
| **Icons & Fonts** | Font Awesome 6.4.0, Google Fonts (Inter) |
| **Responsiveness** | CSS Media Queries |
| **Version Control** | Git |

---

## Project Structure

```
Di_Budol_Website/
├── index.html                  # Main landing page with digital literacy introduction
├── Learning_Center.html        # Educational resources and video tutorials
├── Support.html                # Support services and community resources
├── style.css                   # Unified stylesheet and responsive design
├── Images/                     # Static assets (logo, icons, thumbnails)
└── README.md                   # Project documentation
```

### File Descriptions

- **index.html**: Landing page featuring the platform's mission, digital literacy fundamentals, and engagement opportunities
- **Learning_Center.html**: Central hub for educational content with embedded video tutorials and learning materials
- **Support.html**: Support services directory with counseling, community resources, and crisis contact information
- **style.css**: Comprehensive stylesheet implementing:
  - Dark theme design
  - Smooth animations and transitions
  - Fully responsive layout
  - Accessible color contrasts
  - Card-based UI components

---

## Getting Started

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection for video content and external resources

### Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd Di_Budol_Website
   ```

2. **Open in Browser**
   - Double-click `index.html`, or
   - Use a local server:
     ```bash
     # Python 3
     python -m http.server 8000
     
     # Python 2
     python -m SimpleHTTPServer 8000
     
     # Node.js (with http-server)
     npx http-server
     ```
   - Navigate to `http://localhost:8000`

### File Setup
- Ensure all HTML files are in the root directory
- Place all images in the `Images/` folder
- Verify `style.css` is accessible from all HTML pages

---

## 📖 Usage Guide

### For First-Time Visitors
1. Start at the **Home page** to understand digital literacy and platform mission
2. Explore the **Learning Center** to access tutorials and educational materials
3. Visit **Support** section if assistance is needed
4. Use the **Donate** button to contribute to the cause

### For Educators
- **Learning Materials**: Reference printable guides and tutorials in the Learning Center
- **Community Sessions**: Download and customize materials for group workshops
- **Student Resources**: Share platform links with students for independent learning

### For Support Seekers
- **Crisis Support**: Use the 24/7 contact information in the Support section
- **Counseling Services**: Access mental health and wellness resources
- **Community Help**: Find local assistance and referral programs

---

## 🎨 Design Principles

- **Accessibility**: High contrast ratios and readable typography
- **Responsiveness**: Seamless experience on mobile, tablet, and desktop
- **Simplicity**: Intuitive navigation and clear information hierarchy
- **Engagement**: Visual animations and interactive elements
- **Inclusivity**: Content designed for diverse literacy levels

---

## 🔄 Navigation

```
Home → Learning Center → Support → Contact (available from all pages)
                      ↓
                   Videos
                   ↓
           YouTube embedded content
```

---

## 📝 Content Management

### Adding New Educational Content
1. Create video tutorials and host on YouTube
2. Obtain video thumbnail or screenshot
3. Add new section or card in `Learning_Center.html`:
   ```html
   <div class="video-card">
     <a href="VIDEO_URL" target="_blank">
       <img src="Images/thumbnail.jpg" class="thumbnail" />
     </a>
     <h3>Video Title</h3>
     <p>Video Description</p>
   </div>
   ```
4. Update `style.css` if new styling is needed

### Updating Contact Information
- Edit contact details in `Support.html`
- Update donation links in footer sections

---

## 🌐 External Integrations

- **Google Fonts**: Inter font family for consistent typography
- **Font Awesome**: Icons for UI elements (v6.4.0)
- **YouTube**: Video hosting and embedding for tutorials
- **Filipino Orphans Organization**: Donation and resource links

---

## 💡 Future Enhancements

- **Multi-language Support**: Localization for Tagalog and other languages
- **Interactive Quizzes**: Assessment tools to measure learning
- **Mobile App**: Native iOS/Android applications
- **Community Forum**: Peer-to-peer support and discussion
- **Event Management**: Calendar for workshops and webinars
- **Data Analytics**: Track user engagement and learning outcomes
- **Personalized Learning Paths**: Customized content recommendations
- **Accessibility Improvements**: WCAG 2.1 AA compliance

---

## Support & Contact

For issues, suggestions, or contributions:
- **Website Contact Form**: Use the contact section on the platform
- **24/7 Support Line**: Available through the Support page
- **Email**: Contact through the website portal

---

## License

This project is part of academic coursework and is available under educational use.

---

## Contributors

- Project developed as part of first-year computer science coursework
- Designed to promote digital literacy and community welfare

---

## Development Checklist

- Multi-page responsive website
- Educational content integration
- Smooth animations and transitions
- Mobile-friendly design
- Support resources section
- Community engagement features
- User registration system (future)
- Content management system (future)
- Analytics dashboard (future)
- Multi-language support (future)

---

**Last Updated**: June 2026  
**Version**: 1.0  
**Status**: Active
