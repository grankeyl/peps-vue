export const formatNumber = (value: number) => {
  const absValue = Math.abs(value)
  if (absValue >= 1_000_000_000_000) {
    return Math.floor((value / 1_000_000_000_000) * 10) / 10 + 'T'
  } else if (absValue >= 1_000_000_000) {
    return Math.floor((value / 1_000_000_000) * 10) / 10 + 'B'
  } else if (absValue >= 1_000_000) {
    return Math.floor((value / 1_000_000) * 10) / 10 + 'M'
  } else if (absValue >= 1_000) {
    return Math.floor((value / 1_000) * 10) / 10 + 'K'
  } else {
    return (value * 1).toFixed(0)
  }
}

export function getImage(skin_id: string, format: string = '.png') {
  return '/src/assets/skins/' + skin_id + format
}

export function getRare(type: string, amount: string) {
  if (type == 'views') {
    return 'Views +' + amount + '%'
  } else if (type == 'money') {
    return 'Earn +' + amount + '%'
  } else if (type == 'ton') {
    return 'TON Earn +' + amount + '%'
  } else if (type == 'stamina') {
    return 'Stamina +' + amount + '%'
  }
}
