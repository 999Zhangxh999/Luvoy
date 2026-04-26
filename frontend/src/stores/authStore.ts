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

// 模拟用户数据库
const mockUsers = [
    {
        id: '1',
        username: 'admin',
        email: 'admin@luvoy.com',
        password: 'admin123',
        avatar: '',
        role: 'admin' as const,
        createdAt: '2024-01-01',
    },
    {
        id: '2',
        username: 'maile123',
        email: 'demo@luvoy.com',
        password: '20040916',
        avatar: '',
        role: 'user' as const,
        createdAt: '2024-01-15',
    },
]

// 游客用户
const guestUser: User = {
    id: 'guest',
    username: '游客',
    email: 'guest@luvoy.com',
    avatar: '',
    role: 'user',
    createdAt: new Date().toISOString().split('T')[0],
}

export const useAuthStore = defineStore('auth', () => {
    const user = ref<User | null>(null)
    const token = ref<string | null>(null)
    const loading = ref(false)

    // 计算属性
    const isLoggedIn = computed(() => !!user.value && !!token.value)
    const userInitials = computed(() => {
        if (!user.value) return ''
        return user.value.username.substring(0, 2).toUpperCase()
    })

    // 初始化：从 localStorage 恢复登录状态，或使用游客模式
    function init() {
        const savedToken = localStorage.getItem('luvoy-token')
        const savedUser = localStorage.getItem('luvoy-user')

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

        // 模拟网络延迟
        await new Promise(resolve => setTimeout(resolve, 800))

        // 查找用户
        const foundUser = mockUsers.find(
            u => (u.username === username || u.email === username) && u.password === password
        )

        if (!foundUser) {
            loading.value = false
            throw new Error('用户名或密码错误')
        }

        // 生成模拟 token
        const newToken = `luvoy-${Date.now()}-${Math.random().toString(36).substring(7)}`

        // 设置状态
        user.value = {
            id: foundUser.id,
            username: foundUser.username,
            email: foundUser.email,
            avatar: foundUser.avatar,
            role: foundUser.role,
            createdAt: foundUser.createdAt,
        }
        token.value = newToken

        // 持久化
        if (remember) {
            localStorage.setItem('luvoy-token', newToken)
            localStorage.setItem('luvoy-user', JSON.stringify(user.value))
        } else {
            sessionStorage.setItem('luvoy-token', newToken)
            sessionStorage.setItem('luvoy-user', JSON.stringify(user.value))
        }

        loading.value = false
    }

    // 注册
    async function register(username: string, email: string, password: string): Promise<void> {
        loading.value = true

        // 模拟网络延迟
        await new Promise(resolve => setTimeout(resolve, 800))

        // 检查用户名是否已存在
        if (mockUsers.some(u => u.username === username || u.email === email)) {
            loading.value = false
            throw new Error('用户名或邮箱已被使用')
        }

        // 创建新用户（实际应用中这里应该调用后端 API）
        const newUser = {
            id: String(mockUsers.length + 1),
            username,
            email,
            password,
            avatar: '',
            role: 'user' as const,
            createdAt: new Date().toISOString().split('T')[0],
        }

        mockUsers.push(newUser)

        // 自动登录
        await login(username, password, true)

        loading.value = false
    }

    // 登出
    function logout() {
        user.value = null
        token.value = null

        // 清理存储
        localStorage.removeItem('luvoy-token')
        localStorage.removeItem('luvoy-user')
        sessionStorage.removeItem('luvoy-token')
        sessionStorage.removeItem('luvoy-user')
    }

    // 更新用户信息
    function updateUser(updates: Partial<User>) {
        if (user.value) {
            user.value = { ...user.value, ...updates }

            // 更新存储
            const storage = localStorage.getItem('luvoy-token') ? localStorage : sessionStorage
            storage.setItem('luvoy-user', JSON.stringify(user.value))
        }
    }

    // 检查 token 是否有效
    function checkAuth(): boolean {
        const savedToken = localStorage.getItem('luvoy-token') || sessionStorage.getItem('luvoy-token')
        const savedUser = localStorage.getItem('luvoy-user') || sessionStorage.getItem('luvoy-user')

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
