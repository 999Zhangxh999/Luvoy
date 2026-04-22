/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          // 使用 CSS 变量实现动态主题
          bg: 'var(--brand-bg)',
          surface: 'var(--brand-surface)',
          card: 'var(--brand-card)',
          border: 'var(--brand-border)',
          purple: '#7c3aed',
          violet: '#8b5cf6',
          cyan: '#06b6d4',
          teal: '#14b8a6',
          text: 'var(--brand-text)',
          muted: 'var(--brand-muted)',
          subtle: 'var(--brand-subtle)',
          // 白天模式特有颜色
          primary: 'var(--brand-primary)',
          accent: 'var(--brand-accent)',
        }
      },
      fontFamily: {
        sans: ['Inter', 'PingFang SC', 'Microsoft YaHei', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'grid-pattern': "url(\"data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%231e1e2e' fill-opacity='0.4'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E\")",
      },
      animation: {
        'fade-up': 'fadeUp 0.6s ease forwards',
        'fade-in': 'fadeIn 0.4s ease forwards',
        'glow-pulse': 'glowPulse 3s ease-in-out infinite',
        'typing': 'typing 1.5s steps(20) infinite',
        // 登录页动画
        'glow': 'glow 6s ease-in-out infinite',
        'pulse-slow': 'pulseSlow 8s ease-in-out infinite',
        'float-random': 'floatRandom 10s ease-in-out infinite',
        'float-slow': 'floatSlow 12s ease-in-out infinite',
        'float-spin': 'floatSpin 20s linear infinite',
        'float-spin-light': 'floatSpinLight 15s linear infinite',
        'line-move': 'lineMove 8s ease-in-out infinite',
        'blob': 'blob 15s ease-in-out infinite',
        'twinkle': 'twinkle 3s ease-in-out infinite',
        'float-light-random': 'floatLightRandom 8s ease-in-out infinite',
        'wave': 'wave 10s ease-in-out infinite',
        'gradient-shift': 'gradientShift 8s ease-in-out infinite',
      },
      keyframes: {
        fadeUp: { from: { opacity: '0', transform: 'translateY(20px)' }, to: { opacity: '1', transform: 'translateY(0)' } },
        fadeIn: { from: { opacity: '0' }, to: { opacity: '1' } },
        glowPulse: { '0%,100%': { opacity: '0.6' }, '50%': { opacity: '1' } },
        typing: { '0%,100%': { opacity: '1' }, '50%': { opacity: '0' } },
        // 登录页动画
        glow: {
          '0%, 100%': { opacity: '0.4', transform: 'scale(1)' },
          '50%': { opacity: '0.8', transform: 'scale(1.1)' }
        },
        pulseSlow: {
          '0%, 100%': { opacity: '0.3', transform: 'scale(0.95)' },
          '50%': { opacity: '0.6', transform: 'scale(1.05)' }
        },
        floatRandom: {
          '0%, 100%': { transform: 'translate(0, 0) scale(1)', opacity: '0.6' },
          '25%': { transform: 'translate(10px, -15px) scale(1.1)', opacity: '0.9' },
          '50%': { transform: 'translate(-5px, -25px) scale(0.9)', opacity: '0.7' },
          '75%': { transform: 'translate(-15px, -10px) scale(1.05)', opacity: '0.85' }
        },
        floatSlow: {
          '0%, 100%': { transform: 'translate(0, 0) rotate(0deg)' },
          '33%': { transform: 'translate(15px, -20px) rotate(3deg)' },
          '66%': { transform: 'translate(-10px, 10px) rotate(-3deg)' }
        },
        floatSpin: {
          '0%': { transform: 'rotate(0deg) translateY(0)' },
          '50%': { transform: 'rotate(180deg) translateY(-20px)' },
          '100%': { transform: 'rotate(360deg) translateY(0)' }
        },
        floatSpinLight: {
          '0%': { transform: 'rotate(0deg) scale(1)' },
          '50%': { transform: 'rotate(180deg) scale(1.1)' },
          '100%': { transform: 'rotate(360deg) scale(1)' }
        },
        lineMove: {
          '0%, 100%': { strokeDashoffset: '1000', opacity: '0.2' },
          '50%': { strokeDashoffset: '0', opacity: '0.5' }
        },
        blob: {
          '0%, 100%': { transform: 'translate(-50%, -50%) scale(1) rotate(0deg)' },
          '33%': { transform: 'translate(-50%, -50%) scale(1.1) rotate(120deg)' },
          '66%': { transform: 'translate(-50%, -50%) scale(0.9) rotate(240deg)' }
        },
        twinkle: {
          '0%, 100%': { opacity: '0.4', transform: 'scale(0.8)' },
          '50%': { opacity: '1', transform: 'scale(1.2)' }
        },
        floatLightRandom: {
          '0%, 100%': { transform: 'translateY(0) translateX(0)', opacity: '0.4' },
          '25%': { transform: 'translateY(-20px) translateX(10px)', opacity: '0.7' },
          '50%': { transform: 'translateY(-10px) translateX(-15px)', opacity: '0.5' },
          '75%': { transform: 'translateY(-30px) translateX(5px)', opacity: '0.6' }
        },
        wave: {
          '0%, 100%': { transform: 'translateX(0)' },
          '50%': { transform: 'translateX(-25px)' }
        },
        gradientShift: {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' }
        }
      },
      boxShadow: {
        'glow-purple': '0 0 20px rgba(124,58,237,0.3)',
        'glow-cyan': '0 0 20px rgba(6,182,212,0.3)',
        'card': '0 4px 24px rgba(0,0,0,0.4)',
      }
    },
  },
  plugins: [],
}
