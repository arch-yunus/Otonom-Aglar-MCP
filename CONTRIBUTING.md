# Otonom-Ağlar-MCP Katkıda Bulunma Rehberi

Bu projeye katkıda bulunmak istediğiniz için teşekkürler! Bu repo, Model Context Protocol (MCP) öğrenmek ve otonom sistemler geliştirmek isteyen bir topluluk için tasarlanmıştır.

## Nasıl Katkıda Bulunabilirsiniz?

1. **Hata Bildirimi:** Bir hata bulursanız lütfen [Issue](https://github.com/bahattinyunus/Otonom-Aglar-MCP/issues) açın.
2. **Yeni Özellikler:** Yeni bir MCP sunucusu geliştirdiyseniz (örn: yeni bir API entegrasyonu), PR gönderebilirsiniz.
3. **Dokümantasyon:** Yazım hatalarını düzeltmek veya açıklama eklemek de büyük bir katkıdır.

## Pull Request Süreci

1. Bu repoyu fork'layın.
2. Yeni bir branch oluşturun (`feature/yeni-sunucu` gibi).
3. Değişikliklerinizi yapın.
4. Kodunuzun `mcp-inspector` ile çalıştığından emin olun.
5. PR açın ve neyi neden yaptığınızı açıklayın.

## Kod Standartları

- Sunucu kodlarını `src/` klasörü altına, ilgili modül dizinine ekleyin.
- Her sunucu için docstring ve tip ipuçları (type hints) kullanın.
- Hassas verileri asla koda gömmeyin; `.env` dosyasını kullanın.

---
Mutlu Kodlamalar! 🚀
