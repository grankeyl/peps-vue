import jsonData from '~root/names.json'
import jsonDataSkins from '~root/skinsArray.json'
import jsonDataSpecial from '~root/specialArray.json'
import jsonDataTexts from '~root/textsArray.json'

import moment from 'moment'

export const formatNumber = (value: number) => {
  const absValue = Math.abs(value)
  if (absValue >= 1_000_000_000_000) {
    return Math.floor((value / 1_000_000_000_000) * 10) / 10 + 'T'
  } else if (absValue >= 1_000_000_000) {
    return Math.floor((value / 1_000_000_000) * 10) / 10 + 'B'
  } else if (absValue >= 1_000_000) {
    return Math.floor((value / 1_000_000) * 10) / 10 + 'M'
  } else if (absValue >= 1_000) {
    return Math.floor((value / 1_000) * 10) / 10 + 'k'
  } else {
    return (value * 1).toFixed(0)
  }
}

export function getImage(skin_id: string, format: string = '.png') {
  return '/src/assets/skins/' + skin_id + format
}

export function getRare(language: string, type: string, amount: string) {
  if (type == 'views') {
    if (language == 'ru') {
      return 'Просмотры +' + amount + '%'
    } else {
      return 'Views +' + amount + '%'
    }
  } else if (type == 'money') {
    if (language == 'ru') {
      return 'Заработок +' + amount + '%'
    } else {
      return 'Earn +' + amount + '%'
    }
  } else if (type == 'ton') {
    if (language == 'ru') {
      return 'ТОН Заработок +' + amount + '%'
    } else {
      return 'TON Earn +' + amount + '%'
    }
  } else if (type == 'stamina') {
    if (language == 'ru') {
      return 'Энергия +' + amount + '%'
    } else {
      return 'Stamina +' + amount + '%'
    }
  }
}

export function getSkinInfo(skin_id: string) {
  if (jsonData[skin_id] && jsonData[skin_id].name) {
    return jsonData[skin_id]
  } else {
    return 'None'
  }
}

export function getSkinJson(skin_id) {
  for (const category in jsonDataSkins) {
    const skin = jsonDataSkins[category].versions[skin_id];
    if (skin) {
      return skin;
    }
  }
  return null;
}

export function formatDate(inputDate) {
  const months = [
    'jan',
    'feb',
    'mar',
    'apr',
    'may',
    'jun',
    'jul',
    'aug',
    'sep',
    'oct',
    'nov',
    'dec'
  ]

  const dateParts = inputDate.split(/[- :]/)
  const day = dateParts[0]
  const month = parseInt(dateParts[1]) - 1
  const year = `20${dateParts[2]}`
  const hours = dateParts[3]
  const minutes = dateParts[4]

  return `${day} ${months[month]}, ${hours}:${minutes}`
}

export function requiredXpForPercents(a, b) {
    return (a / b) * 100;
}

export function limitAmount(currentSum, maxSum) {
  return currentSum > maxSum ? maxSum : currentSum
}

export function generateRandomId() {
  const chars = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890'
  let key = ''

  for (let i = 0; i < 9; i++) {
    key += chars.charAt(Math.floor(Math.random() * chars.length))
  }

  return key
}

export function checkDevice(): void {
  const userAgent = navigator.userAgent

  const isDesktop = /Windows|Macintosh|Linux/i.test(userAgent)
  if (isDesktop) {
    return true
  } else {
    return false
  }
}

export function getJsonDataSpecial() {
  return jsonDataSpecial
}

export function getJsonDataTexts() {
  return jsonDataTexts
}

export function startTimerSpecial(targetId: string, targetDate: string) {
  const dateFormat = 'DD-MM-YY HH:mm:ss'
  const startDate = moment(targetDate, dateFormat).toDate()
  const endDate = new Date(startDate.getTime() + 24 * 60 * 60 * 1000)

  async function updateTimer() {
    const now = new Date()
    const timeRemaining = endDate.getTime() - now.getTime()

    console.log(1)

    if (timeRemaining <= 0) {
      document.getElementById(targetId).textContent = '0m 0s'
      clearInterval(timerInterval) // Остановка интервала при достижении 0
      timerRunning = false // Сбрасываем флаг
      return
    } else {
      const days = Math.floor(timeRemaining / (1000 * 60 * 60 * 24))
      const hours = Math.floor((timeRemaining / (1000 * 60 * 60)) % 24)
        .toString()
        .padStart(2, '0')
      const minutes = Math.floor((timeRemaining / (1000 * 60)) % 60)
        .toString()
        .padStart(2, '0')
      const seconds = Math.floor((timeRemaining / 1000) % 60)
        .toString()
        .padStart(2, '0')

      let displayTime = ''

      if (days > 0) {
        displayTime = `${days}d ${hours}h`
      } else if (hours > 0) {
        displayTime = `${hours}h ${minutes}m`
      } else {
        displayTime = `${minutes}m ${seconds}s`
      }

      try {
        document.getElementById(targetId).textContent = displayTime
      } catch {
        return
      }
    }
  }

  updateTimer()
}