import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface User {
    id: string
    username: string
    email: string
    avatar?: string
    role: 'user' | 'admin'
    createdAt: string
}

// 游客用户
const guestUser: User = {
    id: 'guest',
    username: '游客',
    email: 'guest@topo.com',
    avatar: '',
    role: 'user',
    createdAt: new Date().toISOString().split('T')[0],
}

export const useAuthStore = defineStore('auth', () => {
    const user = ref<User | null>(null)
    const token = ref<string | null>(null)
    const loading = ref(false)

    // 计算属性
    const isLoggedIn = computed(() => !!user.value && !!token.value && user.value.id !== 'guest')
    const userInitials = computed(() => {
        if (!user.value) return ''
        return user.value.username.substring(0, 2).toUpperCase()
    })

    // 初始化：从 localStorage 恢复登录状态，或使用游客模式
    function init() {
        const savedToken = localStorage.getItem('topo-token')
        const savedUser = localStorage.getItem('topo-user')

        if (savedToken && savedUser) {
            try {
                token.value = savedToken
                user.value = JSON.parse(savedUser)
            } catch {
                // 解析失败，使用游客模式
                useGuestMode()
            }
        } else {
            // 没有登录信息，默认使用游客模式
            useGuestMode()
        }
    }

    // 游客模式
    function useGuestMode() {
        user.value = { ...guestUser }
        token.value = 'guest-token'
    }

    // 登录
    async function login(username: string, password: string, remember: boolean = false): Promise<void> {
        loading.value = true

        try {
            // 调用后端登录API
            const response = await fetch('http://localhost:5000/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username,
                    password
                })
            })
            
            const data = await response.json()
            if (!data.success) {
                throw new Error(data.message || '登录失败')
            }

            // 设置状态
            user.value = {
                id: String(data.data.user.id),
                username: data.data.user.username,
                email: data.data.user.email,
                avatar: '',
                role: data.data.user.role as 'user' | 'admin',
                createdAt: data.data.user.created_at,
            }
            token.value = data.data.access_token

            // 持久化
            if (remember) {
                localStorage.setItem('topo-token', data.data.access_token)
                localStorage.setItem('topo-user', JSON.stringify(user.value))
            } else {
                sessionStorage.setItem('topo-token', data.data.access_token)
                sessionStorage.setItem('topo-user', JSON.stringify(user.value))
            }
        } catch (error: any) {
            throw new Error(error.message || '登录失败')
        } finally {
            loading.value = false
        }
    }

    // 注册
    async function register(username: string, email: string, password: string): Promise<void> {
        loading.value = true

        try {
            // 调用后端注册API
            const response = await fetch('http://localhost:5000/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username,
                    email,
                    password
                })
            })
            
            const data = await response.json()
            if (!data.success) {
                throw new Error(data.message || '注册失败')
            }

            // 自动登录
            await login(username, password, true)
        } catch (error: any) {
            throw new Error(error.message || '注册失败')
        } finally {
            loading.value = false
        }
    }

    // 登出
    function logout() {
        user.value = null
        token.value = null

        // 清理存储
        localStorage.removeItem('topo-token')
        localStorage.removeItem('topo-user')
        sessionStorage.removeItem('topo-token')
        sessionStorage.removeItem('topo-user')
        
        // 切换到游客模式
        useGuestMode()
    }

    // 更新用户信息
    function updateUser(updates: Partial<User>) {
        if (user.value) {
            user.value = { ...user.value, ...updates }

            // 更新存储
            const storage = localStorage.getItem('topo-token') ? localStorage : sessionStorage
            storage.setItem('topo-user', JSON.stringify(user.value))
        }
    }

    // 检查 token 是否有效
    function checkAuth(): boolean {
        const savedToken = localStorage.getItem('topo-token') || sessionStorage.getItem('topo-token')
        const savedUser = localStorage.getItem('topo-user') || sessionStorage.getItem('topo-user')

        if (!savedToken || !savedUser) {
            logout()
            return false
        }

        if (!token.value || !user.value) {
            init()
        }

        return isLoggedIn.value
    }

    // 初始化
    init()

    return {
        user,
        token,
        loading,
        isLoggedIn,
        userInitials,
        login,
        register,
        logout,
        updateUser,
        checkAuth,
        init,
        useGuestMode,
    }
})