<?php
/**
 * Wiccom · Receptor de formularios (contacto, cotización, asesor, marca/producto)
 * Responde JSON: {"ok": true|false, "message": "..."}
 * Configura los correos de destino abajo. Requiere mail() habilitado en el hosting
 * (en producción se recomienda PHPMailer + SMTP autenticado).
 */
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('X-Content-Type-Options: nosniff');

// ================= CONFIGURACIÓN =================
const DESTINO      = 'danaeearrieta@gmail.com';        // quién recibe
const DESTINO_CC   = 'tecnologia8@globalbtek.com';      // copia (déjalo '' si no aplica)
const REMITENTE    = 'no-reply@wiccom.com.mx';    // debe ser del mismo dominio del hosting
const MAX_BYTES    = 10 * 1024 * 1024;            // 10 MB por archivo
const MAX_ARCHIVOS = 5;
const MIN_SEGUNDOS = 3;                           // tiempo mínimo para llenar (anti-bots)
const EXT_OK = ['pdf','doc','docx','xls','xlsx','jpg','jpeg','png','dwg'];
// =================================================

function responder(bool $ok, string $msg, int $code = 200): never {
  http_response_code($code);
  echo json_encode(['ok' => $ok, 'message' => $msg], JSON_UNESCAPED_UNICODE);
  exit;
}
function limpio(string $k, int $max = 200): string {
  $v = trim((string)($_POST[$k] ?? ''));
  $v = str_replace(["\r", "\n", "%0a", "%0d"], ' ', $v); // evita inyección de cabeceras
  return mb_substr(strip_tags($v), 0, $max);
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') responder(false, 'Método no permitido.', 405);

// Honeypot + tiempo mínimo
if (!empty($_POST['website'])) responder(true, 'Gracias.');
$ts = (int)($_POST['_ts'] ?? 0);
if ($ts > 0 && (time() * 1000 - $ts) < MIN_SEGUNDOS * 1000) responder(false, 'Envío demasiado rápido, intenta de nuevo.', 429);

$form      = limpio('form', 40) ?: 'contacto';
$nombre    = limpio('nombre', 120);
$empresa   = limpio('empresa', 120);
$correo    = filter_var(limpio('correo', 160), FILTER_VALIDATE_EMAIL) ?: '';
$telefono  = preg_replace('/[^0-9+\s()-]/', '', limpio('telefono', 30));
$interes   = limpio('interes', 120);
$tipo      = limpio('tipo', 120);
$ciudad    = limpio('ciudad', 120);
$marca     = limpio('marca', 120);
$modelo    = limpio('modelo', 160);
$contexto  = limpio('contexto', 200);
$mensaje   = mb_substr(strip_tags(trim((string)($_POST['mensaje'] ?? ''))), 0, 2000);

if ($nombre === '' || ($correo === '' && $telefono === '')) responder(false, 'Faltan datos obligatorios.', 422);
if (isset($_POST['privacidad']) === false && $form !== 'asesor') responder(false, 'Debes aceptar el Aviso de Privacidad.', 422);

// Cuerpo del correo
$filas = [
  'Formulario' => $form, 'Página' => $contexto, 'Nombre' => $nombre, 'Empresa' => $empresa,
  'Correo' => $correo, 'Teléfono' => $telefono, 'Interés / servicio' => $interes ?: $tipo,
  'Ciudad / Estado' => $ciudad, 'Marca' => $marca, 'Modelo / producto' => $modelo,
];
$html = '<h2 style="font-family:Arial;color:#0D1B2A">Nueva solicitud desde wiccom.com.mx</h2><table cellpadding="6" style="font-family:Arial;font-size:14px;border-collapse:collapse">';
foreach ($filas as $k => $v) if ($v !== '') $html .= '<tr><td style="color:#667085"><b>'.$k.'</b></td><td>'.htmlspecialchars($v).'</td></tr>';
$html .= '</table><p style="font-family:Arial;font-size:14px"><b>Mensaje:</b><br>'.nl2br(htmlspecialchars($mensaje)).'</p>';

// Adjuntos
$adjuntos = [];
if (!empty($_FILES['archivos']) && is_array($_FILES['archivos']['name'])) {
  $n = min(count($_FILES['archivos']['name']), MAX_ARCHIVOS);
  $finfo = new finfo(FILEINFO_MIME_TYPE);
  for ($i = 0; $i < $n; $i++) {
    if ($_FILES['archivos']['error'][$i] !== UPLOAD_ERR_OK) continue;
    $tmp  = $_FILES['archivos']['tmp_name'][$i];
    $name = preg_replace('/[^\w.\- ]/u', '_', basename($_FILES['archivos']['name'][$i]));
    $ext  = strtolower(pathinfo($name, PATHINFO_EXTENSION));
    if (!in_array($ext, EXT_OK, true) || filesize($tmp) > MAX_BYTES || !is_uploaded_file($tmp)) continue;
    $adjuntos[] = ['name' => $name, 'mime' => $finfo->file($tmp) ?: 'application/octet-stream', 'data' => file_get_contents($tmp)];
  }
}

// MIME
$asunto = '=?UTF-8?B?'.base64_encode('Wiccom · '.ucfirst($form).' · '.$nombre).'?=';
$b = 'wc_'.bin2hex(random_bytes(8));
$headers  = 'From: Sitio Wiccom <'.REMITENTE.">\r\n";
if ($correo) $headers .= 'Reply-To: '.$correo."\r\n";
if (DESTINO_CC) $headers .= 'Cc: '.DESTINO_CC."\r\n";
$headers .= "MIME-Version: 1.0\r\nContent-Type: multipart/mixed; boundary=\"$b\"\r\n";
$body  = "--$b\r\nContent-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n".chunk_split(base64_encode($html));
foreach ($adjuntos as $a) {
  $body .= "--$b\r\nContent-Type: {$a['mime']}; name=\"{$a['name']}\"\r\nContent-Transfer-Encoding: base64\r\nContent-Disposition: attachment; filename=\"{$a['name']}\"\r\n\r\n".chunk_split(base64_encode($a['data']));
}
$body .= "--$b--";

if (@mail(DESTINO, $asunto, $body, $headers, '-f'.REMITENTE)) {
  responder(true, '¡Gracias! Un asesor se pondrá en contacto contigo muy pronto.');
}
responder(false, 'No pudimos enviar tu solicitud en este momento.', 500);
